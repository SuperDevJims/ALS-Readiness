from sqlalchemy import select

from app.models.strand_test import StrandTestItem, StrandTestItemOption

from .base import BaseRepository


class StrandTestItemOptionRepository(BaseRepository[StrandTestItemOption]):
    model = StrandTestItemOption

    async def get_by_test(self, test_id: int) -> list[StrandTestItemOption]:
        statement = (
            select(StrandTestItemOption)
            .join(StrandTestItem, StrandTestItem.id == StrandTestItemOption.item_id)
            .where(StrandTestItem.test_id == test_id)
        )
        result = await self._session.execute(statement)
        return list(result.scalars().all())