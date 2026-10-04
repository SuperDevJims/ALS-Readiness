from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    ContentAlreadyAssignedError,
    ContentNotAssignedError,
    ContentNotFoundError,
)
from app.enums.content import ContentStatus
from app.models.cohort_content import CohortContent
from app.models.user import User
from app.repositories.cohort_content import CohortContentRepository
from app.repositories.content import ContentRepository
from app.services.facilitator_scope import FacilitatorScopeService


class CohortContentService:
    """Switches content on and off for a cohort (D13). Writes need an active cohort (D17)."""

    def __init__(
        self,
        cohort_content_repo: CohortContentRepository,
        content_repo: ContentRepository,
        facilitator_scope_service: FacilitatorScopeService,
    ):
        self._cohort_content_repo = cohort_content_repo
        self._content_repo = content_repo
        self._facilitator_scope_service = facilitator_scope_service

    async def assign(self, user: User, cohort_id: int, content_id: int) -> CohortContent:
        await self._facilitator_scope_service.assert_cohort_writable(user, cohort_id)

        # Missing, inactive, and someone else's private content all get the same
        # 404, so a private item's existence is not revealed.
        content = await self._content_repo.get_by_id(content_id)
        if (
            content is None
            or content.status != ContentStatus.ACTIVE
            or not await self._facilitator_scope_service.can_see_content(user, content)
        ):
            raise ContentNotFoundError()

        # The unique constraint is the backstop; this check is what makes the
        # failure a clean 409.
        existing = await self._cohort_content_repo.get_by_cohort_id_and_content_id(
            cohort_id, content_id
        )
        if existing is not None:
            raise ContentAlreadyAssignedError()

        try:
            return await self._cohort_content_repo.create(
                CohortContent(cohort_id=cohort_id, content_id=content_id, assigned_by=user.id)
            )
        except IntegrityError:
            # A concurrent assignment got past the check above.
            raise ContentAlreadyAssignedError() from None

    async def unassign(self, user: User, cohort_id: int, content_id: int) -> None:
        await self._facilitator_scope_service.assert_cohort_writable(user, cohort_id)

        assignment = await self._cohort_content_repo.get_by_cohort_id_and_content_id(
            cohort_id, content_id
        )
        if assignment is None:
            raise ContentNotAssignedError()

        # Learners' progress rows for this content are left as they are.
        await self._cohort_content_repo.delete(assignment)
