from sqlalchemy import select

from app.models.facilitator import Facilitator

from .base import BaseRepository


class FacilitatorRepository(BaseRepository[Facilitator]):
    model = Facilitator

    async def get_by_user_id(self, user_id: int) -> Facilitator | None:
        statement = select(Facilitator).where(Facilitator.user_id == user_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
    