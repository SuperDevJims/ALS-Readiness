from sqlalchemy import select

from app.enums.cohort import CohortStatus
from app.models.cohort import Cohort, CohortFacilitator, CohortLearner
from app.models.facilitator import Facilitator
from app.models.learner import Learner
from app.models.user import User

from .base import BaseRepository


class CohortRepository(BaseRepository[Cohort]):
    model = Cohort

    async def get_by_status(self, status: CohortStatus) -> list[Cohort]:
        statement = select(Cohort).where(Cohort.status == status)
        result = await self._session.execute(statement)
        return list(result.scalars().all())

    async def get_all(self) -> list[Cohort]:
        result = await self._session.execute(select(Cohort))
        return list(result.scalars().all())

    async def get_cohort_by_learner_user_id(self, user_id: int) -> Cohort | None:
        statement = (
            select(Cohort)
            .join(CohortLearner, Cohort.id == CohortLearner.cohort_id)
            .join(Learner, Learner.id == CohortLearner.learner_id)
            .join(User, User.id == Learner.user_id)
            .where(User.id == user_id)
        )

        result = await self._session.execute(statement)
        return result.scalars().first()

    async def get_cohort_by_facilitator_id(self, user_id: int) -> list[Cohort]:
        statement = (
            select(Cohort)
            .join(CohortFacilitator, Cohort.id == CohortFacilitator.cohort_id)
            .join(Facilitator, Facilitator.id == CohortFacilitator.facilitator_id)
            .join(User, User.id == Facilitator.user_id)
            .where(User.id == user_id)
        )

        result = await self._session.execute(statement)
        return list(result.scalars().all())
