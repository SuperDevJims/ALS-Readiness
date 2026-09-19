from sqlalchemy import select

from app.models.lri_test_attempt import LRITestAttempt

from .base import BaseRepository


class LRITestAttemptRepository(BaseRepository[LRITestAttempt]):
    model = LRITestAttempt

    async def get_by_test_and_learner(
        self, test_id: int, learner_id: int
    ) -> LRITestAttempt | None:
        """The learner's own attempt for a test. If duplicates exist (no unique
        constraint yet), the earliest one is the authoritative submission."""
        statement = (
            select(LRITestAttempt)
            .where(
                LRITestAttempt.test_id == test_id,
                LRITestAttempt.learner_id == learner_id,
            )
            .order_by(LRITestAttempt.id)
            .limit(1)
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
    