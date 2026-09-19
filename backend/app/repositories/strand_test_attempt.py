from sqlalchemy import select

from app.enums.strand_test import StrandTestType
from app.models.strand_test import StrandTest
from app.models.strand_test_attempt import StrandTestAttempt

from .base import BaseRepository


class StrandTestAttemptRepository(BaseRepository[StrandTestAttempt]):
    model = StrandTestAttempt

    async def get_by_test_and_learner(
        self, test_id: int, learner_id: int
    ) -> StrandTestAttempt | None:
        """The learner's own attempt for a test. If duplicates exist (no unique
        constraint yet), the earliest one is the authoritative submission."""
        statement = (
            select(StrandTestAttempt)
            .where(
                StrandTestAttempt.test_id == test_id,
                StrandTestAttempt.learner_id == learner_id,
            )
            .order_by(StrandTestAttempt.id)
            .limit(1)
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def has_pretest_attempt(self, learner_id: int, strand_id: int) -> bool:
        """Whether the learner has attempted the pretest of the given strand."""
        statement = (
            select(StrandTestAttempt.id)
            .join(StrandTest, StrandTest.id == StrandTestAttempt.test_id)
            .where(
                StrandTestAttempt.learner_id == learner_id,
                StrandTest.strand_id == strand_id,
                StrandTest.type == StrandTestType.PRETEST.value,
            )
            .limit(1)
        )
        result = await self._session.execute(statement)
        return result.first() is not None
