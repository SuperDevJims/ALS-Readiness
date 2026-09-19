from sqlalchemy import select

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
