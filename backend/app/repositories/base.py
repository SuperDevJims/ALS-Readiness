from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


class BaseRepository[ModelT: SQLModel]:
    """Serves as the base parent that provides common methods and initialization to repositories."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, instance: ModelT) -> ModelT:
        self._session.add(instance)

        await self._session.flush()
        await self._session.refresh(instance)

        return instance

    async def get_by_id(self, entity_id: int) -> ModelT | None:
        return await self._session.get(self.model, entity_id)

    async def update(
    self,
    instance: ModelT,
    data: dict[str, Any],
    ) -> ModelT:
        instance.sqlmodel_update(data)

        await self._session.flush()
        await self._session.refresh(instance)

        return instance

    async def rollback(self) -> None:
        """Allows handler to undo any pending changes in the current transactions."""
        self._session.rollback()

    async def commit(self) -> None:
        """Allows handler to save changes to the database."""
        self._session.commit()
