from sqlalchemy import select

from app.models.learner import Learner

from .base import BaseRepository


class LearnerRepository(BaseRepository[Learner]):

    model = Learner

    async def get_by_user_id(self, user_id: int) -> Learner | None:
        statement = select(Learner).where(Learner.user_id == user_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none