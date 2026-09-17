from typing import Any

from sqlalchemy import func, select

from app.enums.user import UserRole
from app.models.user import User
from app.models.user_profile import UserProfile

from .base import BaseRepository


class UserRepository(BaseRepository[User]):

    model = User

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def list_with_profiles(
        self,
        page: int,
        page_size: int,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[tuple[User, UserProfile | None]], int]:
        conditions = []
        if role is not None:
            conditions.append(User.role == role)
        if is_active is not None:
            conditions.append(User.is_active == is_active)

        count_statement = select(func.count()).select_from(User)
        if conditions:
            count_statement = count_statement.where(*conditions)

        total = (await self._session.execute(count_statement)).scalar_one()

        statement = (
            select(User, UserProfile)
            .outerjoin(UserProfile, UserProfile.user_id == User.id)
            .order_by(User.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        if conditions:
            statement = statement.where(*conditions)

        result = await self._session.execute(statement)
        rows = [(row[0], row[1]) for row in result.all()]

        return rows, total

    async def get_by_id_no(self, id_no: str) -> User | None:
        statement = select(User).where(User.id_no == id_no)
        result = await self._session.execute(statement)

        return result.scalar_one_or_none()
    
    async def update(self, user: User, fields: dict[str, Any]) -> User:
        user.sqlmodel_update(fields)

        await self._session.flush()
        await self._session.refresh(user)

        return user
