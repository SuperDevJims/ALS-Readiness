from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


class BaseRepository[ModelT: SQLModel]:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: ModelT) -> ModelT:
        self._session.add(data)

        await self._session.flush()
        await self._session.refresh(data)

        return data

    async def get_by_id(self, id: int) -> ModelT | None:
        return await self._session.get(self.model, id)
