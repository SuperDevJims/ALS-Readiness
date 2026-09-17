from app.models.participant_intake import ParticipantIntake
from app.schemas.participant_intake import ParticipantIntakeUpsert

from .base import BaseRepository


class ParticipantIntakeRepository(BaseRepository[ParticipantIntake]):
    model = ParticipantIntake

    async def get_by_user_id(self, user_id: int) -> ParticipantIntake | None:
        return await self._session.get(ParticipantIntake, user_id)

    async def update(self, intake: ParticipantIntake, data: ParticipantIntakeUpsert) -> ParticipantIntake:
        intake.sqlmodel_update(data.model_dump())
        await self._session.flush()
        await self._session.refresh(intake)
        return intake
