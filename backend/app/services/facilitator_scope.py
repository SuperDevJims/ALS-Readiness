from collections.abc import Callable

from app.core.exceptions import (
    CohortAccessDeniedError,
    CohortNotActiveError,
    CohortNotFoundError,
)
from app.enums.cohort import CohortStatus
from app.enums.content import ContentVisibility
from app.enums.user import UserRole
from app.models.cohort import Cohort
from app.models.content import Content
from app.models.user import User
from app.repositories.cohort import CohortRepository
from app.repositories.cohort_learner import CohortLearnerRepository
from app.repositories.facilitator import FacilitatorRepository

# A facilitator can see a cohort in any of these states. An archived cohort is
# hidden from facilitators even while their assignment to it is still active.
VISIBLE_COHORT_STATUSES = (
    CohortStatus.UPCOMING,
    CohortStatus.ACTIVE,
    CohortStatus.COMPLETED,
)


class FacilitatorScopeService:
    """Decides which cohorts and learners a caller may see, and which cohorts
    they may change.

    An admin may see everything. A facilitator may see a cohort when their
    assignment to it is active and the cohort is not archived, and may see the
    learners in those cohorts. Anyone else is denied. Changes are allowed only
    while the cohort itself is active.

    Content follows D9: a facilitator sees their own uploads plus other
    facilitators' public content.
    """

    def __init__(
        self,
        cohort_repo: CohortRepository,
        cohort_learner_repo: CohortLearnerRepository,
        facilitator_repo: FacilitatorRepository,
    ):
        self._cohort_repo = cohort_repo
        self._cohort_learner_repo = cohort_learner_repo
        self._facilitator_repo = facilitator_repo

    async def get_visible_cohorts(self, user: User) -> list[Cohort]:
        if user.role != UserRole.FACILITATOR:
            return []

        cohorts = await self._cohort_repo.get_cohort_by_facilitator_id(user.id)
        return [cohort for cohort in cohorts if cohort.status in VISIBLE_COHORT_STATUSES]

    async def get_visible_cohort_ids(self, user: User) -> list[int]:
        return [cohort.id for cohort in await self.get_visible_cohorts(user)]

    async def assert_cohort_access(self, user: User, cohort_id: int) -> None:
        if user.role == UserRole.ADMIN:
            return

        if cohort_id not in await self.get_visible_cohort_ids(user):
            raise CohortAccessDeniedError()

    async def assert_cohort_writable(self, user: User, cohort_id: int) -> None:
        await self.assert_cohort_access(user, cohort_id)

        cohort = await self._cohort_repo.get_by_id(cohort_id)
        if cohort is None:
            # Only an admin gets this far for a cohort that does not exist.
            raise CohortNotFoundError()

        if cohort.status != CohortStatus.ACTIVE:
            raise CohortNotActiveError()

    async def assert_learner_access(self, user: User, learner_id: int) -> None:
        if user.role == UserRole.ADMIN:
            return

        # Ended memberships count, so a facilitator can still view a learner
        # who completed one of the cohorts they can see.
        cohort_ids = await self.get_visible_cohort_ids(user)
        if not await self._cohort_learner_repo.exists_in_cohorts(learner_id, cohort_ids):
            raise CohortAccessDeniedError()

    async def get_content_filter(self, user: User) -> Callable[[Content], bool]:
        """A predicate telling whether the caller may see a content item (D9).

        Built once per request, so a whole tree can be filtered with one lookup.
        Status is not considered here; callers filter on it separately.
        """
        if user.role == UserRole.ADMIN:
            return lambda content: True

        if user.role != UserRole.FACILITATOR:
            return lambda content: False

        facilitator = await self._facilitator_repo.get_by_user_id(user.id)
        facilitator_id = facilitator.id if facilitator is not None else None

        def is_visible(content: Content) -> bool:
            return content.visibility == ContentVisibility.PUBLIC or (
                facilitator_id is not None and content.uploaded_by == facilitator_id
            )

        return is_visible

    async def can_see_content(self, user: User, content: Content) -> bool:
        return (await self.get_content_filter(user))(content)
