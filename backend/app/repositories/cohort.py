from sqlalchemy import select

from app.enums.cohort import CohortStatus
from app.models.cohort import Cohort

from .base import BaseRepository


class CohortRepository(BaseRepository[Cohort]):
    model = Cohort

    async def get_by_status(self, status: CohortStatus) -> list[Cohort]:
        statement = select(Cohort).where(Cohort.status == status)
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def get_all(self) -> list[Cohort]:
        result = await self._session.execute(select(Cohort))
        return result.scalars().all()
