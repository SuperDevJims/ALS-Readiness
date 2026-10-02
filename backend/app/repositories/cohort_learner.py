from sqlalchemy import select

from app.models.cohort import CohortLearner
from app.models.learner import Learner
from app.models.user import User
from app.models.user_profile import UserProfile
from app.enums.cohort import CohortMemberStatus

from .base import BaseRepository


class CohortLearnerRepository(BaseRepository[CohortLearner]):
    model = CohortLearner

    async def get_by_cohort_id_and_learner_id(
        self,
        cohort_id: int,
        learner_id: int,
    ) -> CohortLearner | None:
        statement = select(CohortLearner).where(
            CohortLearner.cohort_id == cohort_id,
            CohortLearner.learner_id == learner_id,
        )
        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_all_by_cohort_id_with_profile(
        self, 
        cohort_id: int
    ) -> list[tuple[CohortLearner, UserProfile]]:
        statement = (
            select(CohortLearner, UserProfile)
            .join(Learner, Learner.id == CohortLearner.learner_id)
            .join(User, User.id == Learner.user_id)
            .join(UserProfile, UserProfile.user_id == User.id)
            .where(CohortLearner.cohort_id == cohort_id)
        )
        result = await self._session.execute(statement)
        return result.all()

    async def get_active_by_learner_id(self, learner_id: int) -> CohortLearner | None:
        statement = (
            select(CohortLearner)
            .where(
                CohortLearner.learner_id == learner_id, 
                CohortLearner.status == CohortMemberStatus.ACTIVE,
            )
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def exists_in_cohorts(self, learner_id: int, cohort_ids: list[int]) -> bool:
        """Whether the learner has a membership, active or ended, in any of the cohorts."""
        if not cohort_ids:
            return False

        statement = (
            select(CohortLearner.id)
            .where(
                CohortLearner.learner_id == learner_id,
                CohortLearner.cohort_id.in_(cohort_ids),
            )
            .limit(1)
        )
        result = await self._session.execute(statement)
        return result.first() is not None
