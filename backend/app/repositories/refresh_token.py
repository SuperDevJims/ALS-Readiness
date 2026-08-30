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
