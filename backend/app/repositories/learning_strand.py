from sqlalchemy import select

from app.models.learning_strand import LearningStrand

from .base import BaseRepository


class LearningStrandRepository(BaseRepository[LearningStrand]):
    model = LearningStrand

    async def get_by_code(self, code: str) -> LearningStrand | None:
        statement = select(LearningStrand).where(LearningStrand.code == code)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
