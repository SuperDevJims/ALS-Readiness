from sqlalchemy import select

from app.models.lri_test import LRITest, LRITestItem
from app.models.lri_test_attempt import LRITestAttempt

from .base import BaseRepository


class LRITestRepository(BaseRepository[LRITest]):
    model = LRITest

    async def get_with_attempt(self, learner_id) -> LRITest | None:
        statement = (
            select(LRITest, LRITestAttempt)
            .outerjoin(
                LRITestAttempt, 
                (LRITestAttempt.test_id == LRITest.id) 
                & (LRITestAttempt.learner_id == learner_id)
            )
        )
        result = await self._session.execute(statement)
        return result.one_or_none()

    async def get_by_id_with_items(self, test_id: int) -> list[tuple[LRITest, LRITestItem]]:
        statement = (
            select(LRITest, LRITestItem)
            .join(LRITestItem, LRITestItem.test_id == LRITest.id)
            .where(LRITest.id == test_id)
        )
        result = await self._session.execute(statement)
        return result.all()
