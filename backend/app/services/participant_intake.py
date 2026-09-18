from datetime import datetime, timezone

from app.models.participant_intake import ParticipantIntake
from app.repositories.participant_intake import ParticipantIntakeRepository
from app.schemas.participant_intake import ParticipantIntakeUpsert


class ParticipantIntakeService:
    def __init__(self, repository: ParticipantIntakeRepository):
        self._repository = repository

    async def get_by_user_id(self, user_id: int) -> ParticipantIntake | None:
        return await self._repository.get_by_user_id(user_id)

    async def upsert(self, user_id: int, data: ParticipantIntakeUpsert) -> ParticipantIntake:
        intake = await self.get_by_user_id(user_id)
        if intake is not None:
            return await self._repository.update(intake, data)

        return await self._repository.create(
            ParticipantIntake(user_id=user_id, submitted_at=datetime.now(timezone.utc), **data.model_dump())
        )
