from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from app.models.refresh_token import RefreshToken

from .base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    model = RefreshToken

    async def get_by_jti(self, jti: UUID) -> RefreshToken | None:
        statement = select(RefreshToken).where(RefreshToken.jti == jti)

        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def revoke(self, jti: UUID, revoked_at: datetime) -> None:

        refresh_token = await self.get_by_jti(jti)

        refresh_token.is_revoked = True
        refresh_token.revoked_at = revoked_at

        await self._session.flush()

    async def revoke_all_for_user(self, user_id: int, revoked_at: datetime) -> None:
        statement = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked.is_(False),
        )
        result = await self._session.execute(statement)

        for refresh_token in result.scalars():
            refresh_token.is_revoked = True
            refresh_token.revoked_at = revoked_at

        await self._session.flush()

    async def revoke_all_for_user_except(
        self, user_id: int, except_jti: UUID, revoked_at: datetime
    ) -> None:
        statement = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked.is_(False),
            RefreshToken.jti != except_jti,
        )
        result = await self._session.execute(statement)

        for refresh_token in result.scalars():
            refresh_token.is_revoked = True
            refresh_token.revoked_at = revoked_at

        await self._session.flush()
