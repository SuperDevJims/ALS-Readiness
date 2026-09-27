# app/repositories/curriculum.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.content import Content
from app.models.learner_content_progress import LearnerContentProgress
from app.models.learning_strand import LearningStrand
from app.models.lesson import Lesson
from app.models.module import Module


class CurriculumRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_strand_tree(self, strand_id: int) -> LearningStrand | None:
        statement = (
            select(LearningStrand)
            .where(LearningStrand.id == strand_id)
            .options(
                selectinload(LearningStrand.modules)
                .selectinload(Module.lessons)
                .selectinload(Lesson.contents)
                .selectinload(Content.evaluation)
            )
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_progress_map(
        self,
        learner_id: int,
        content_ids: list[int],
    ) -> dict[int, LearnerContentProgress]:
        if not content_ids:
            return {}

        statement = select(LearnerContentProgress).where(
            LearnerContentProgress.learner_id == learner_id,
            LearnerContentProgress.content_id.in_(content_ids),
        )
        result = await self._session.execute(statement)
        return {row.content_id: row for row in result.scalars()}
