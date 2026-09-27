from sqlalchemy import select

from app.models.cohort_content import CohortContent

from .base import BaseRepository


class CohortContentRepository(BaseRepository[CohortContent]):
    model = CohortContent

    async def get_content_ids(self, cohort_id: int) -> list[int]:
        stmt = select(CohortContent.content_id).where(CohortContent.cohort_id == cohort_id)
        result = await self._session.execute(stmt)
        return list(result.scalars())
