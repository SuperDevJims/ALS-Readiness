from app.core.exceptions import (
    CohortLearnerAlreadyExistsError,
    CohortLearnerNotFoundError,
)
from app.enums.cohort import CohortMemberStatus
from app.models.cohort import CohortLearner
from app.models.learner import Learner
from app.models.user_profile import UserProfile
from app.repositories.cohort_learner import CohortLearnerRepository
from app.services.learner import LearnerService


class CohortLearnerService:
    def __init__(
        self,
        cohort_learner_repo: CohortLearnerRepository,
        learner_service: LearnerService,
    ):
        self._cohort_learner_repo = cohort_learner_repo
        self._learner_service = learner_service

    async def create(
        self,
        admin_id: int,
        cohort_id: int,
        learner_id: int,
    ) -> CohortLearner:
        _ = await self._learner_service.get_by_id(learner_id)

        existing = await self._cohort_learner_repo.get_by_cohort_id_and_learner_id(
            cohort_id, learner_id
        )

        if existing:
            raise CohortLearnerAlreadyExistsError()

        cohort_learner = CohortLearner(
            assigned_by=admin_id,
            learner_id=learner_id,
            cohort_id=cohort_id,
        )

        created_cohort_learner = await self._cohort_learner_repo.create(cohort_learner)

        return created_cohort_learner

    async def get_all_by_cohort_id_with_profile(
        self,
        cohort_id: int,
    ) -> list[tuple[CohortLearner, UserProfile]]:
        return await (
            self._cohort_learner_repo
            .get_all_by_cohort_id_with_profile(cohort_id)
        )

    async def update_status(self, cohort_learner_id: int, status: CohortMemberStatus) -> CohortLearner:
        cohort_learner = await self._cohort_learner_repo.get_by_id(cohort_learner_id)

        if cohort_learner is None:
            raise CohortLearnerNotFoundError()

        return await self._cohort_learner_repo.update(cohort_learner, {"status": status})
