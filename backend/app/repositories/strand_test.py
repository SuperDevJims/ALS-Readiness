from sqlalchemy import select

from app.enums.strand_test import StrandTestType
from app.models.curriculum import LearningStrand
from app.models.strand_test import StrandTest, StrandTestItem, StrandTestItemOption
from app.models.strand_test_attempt import StrandTestAttempt

from .base import BaseRepository


class StrandTestRepository(BaseRepository[StrandTest]):
    model = StrandTest

    async def get_by_type_with_attempt(self, learner_id: int, test_type: StrandTestType):
        """Get strand tests with their learning strand and the learner's attempt."""

        statement = (
            select(StrandTest, LearningStrand, StrandTestAttempt)
            .join(LearningStrand, LearningStrand.id == StrandTest.strand_id)
            .outerjoin(
                StrandTestAttempt,
                (StrandTestAttempt.test_id == StrandTest.id)
                & (StrandTestAttempt.learner_id == learner_id),
            )
            .where(StrandTest.type == test_type.value)
        )

        result = await self._session.execute(statement)
        return result.all()

    async def get_by_id(self, test_id: int) -> StrandTest:
        statement = select(StrandTest).where(StrandTest.id == test_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id_with_items(self, test_id: int) -> list[tuple[StrandTest, StrandTestItem, StrandTestItemOption]]:
        statement = (
            select(StrandTest, StrandTestItem, StrandTestItemOption)
            .join(StrandTestItem, StrandTestItem.test_id == StrandTest.id)
            .join(StrandTestItemOption, StrandTestItemOption.item_id == StrandTestItem.id)
            .where(StrandTest.id == test_id)
        )

        result = await self._session.execute(statement)
        return result.all()
    

"""
statement = (
    select(StrandTest, LearningStrand, StrandTestAttempt)
    .join(LearningStrand, LearningStrand.id == StrandTest.strand_id)
    .outerjoin(
        StrandTestAttempt,
        (StrandTestAttempt.test_id == StrandTest.id)
        & (StrandTestAttempt.learner_id == learner_id),
    )
    .where(StrandTest.type == type.value)
)
"""