from typing import Any

from sqlalchemy import select

from app.models.user import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    
    model = User

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_id_no(self, id_no: str) -> User | None:
        statement = select(User).where(User.id_no == id_no)
        result = await self._session.execute(statement)

        return result.scalar_one_or_none()
    
    async def update(self, user: User, fields: dict[str, Any]) -> User:
        user.sqlmodel_update(fields)

        await self._session.flush()
        await self._session.refresh(user)

        return user
