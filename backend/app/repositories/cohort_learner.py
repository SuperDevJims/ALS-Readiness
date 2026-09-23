from sqlalchemy import select

from app.models.cohort import CohortLearner
from app.models.learner import Learner
from app.models.user import User
from app.models.user_profile import UserProfile

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
