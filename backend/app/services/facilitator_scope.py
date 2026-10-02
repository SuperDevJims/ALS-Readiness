from app.core.exceptions import CohortAccessDeniedError
from app.enums.user import UserRole
from app.models.user import User
from app.repositories.cohort_facilitator import CohortFacilitatorRepository
from app.repositories.cohort_learner import CohortLearnerRepository


class FacilitatorScopeService:
    """Decides which cohorts and learners a caller may see.

    An admin may see everything. A facilitator may see the cohorts they are
    actively assigned to and the learners in them. Anyone else is denied.
    """

    def __init__(
        self,
        cohort_facilitator_repo: CohortFacilitatorRepository,
        cohort_learner_repo: CohortLearnerRepository,
    ):
        self._cohort_facilitator_repo = cohort_facilitator_repo
        self._cohort_learner_repo = cohort_learner_repo

    async def get_active_cohort_ids(self, user: User) -> list[int]:
        if user.role != UserRole.FACILITATOR:
            return []

        return await self._cohort_facilitator_repo.get_active_cohort_ids_by_user_id(user.id)

    async def assert_cohort_access(self, user: User, cohort_id: int) -> None:
        if user.role == UserRole.ADMIN:
            return

        if cohort_id not in await self.get_active_cohort_ids(user):
            raise CohortAccessDeniedError()

    async def assert_learner_access(self, user: User, learner_id: int) -> None:
        if user.role == UserRole.ADMIN:
            return

        # Ended memberships count, so a facilitator can still view a learner
        # who completed one of their cohorts.
        cohort_ids = await self.get_active_cohort_ids(user)
        if not await self._cohort_learner_repo.exists_in_cohorts(learner_id, cohort_ids):
            raise CohortAccessDeniedError()
