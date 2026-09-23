from app.core.exceptions import FacilitatorNotFoundError
from app.models.facilitator import Facilitator
from app.repositories.facilitator import FacilitatorRepository
from app.schemas.facilitator import FacilitatorCreate


class FacilitatorService:
    def __init__(self, facilitator_repository: FacilitatorRepository):
        self._facilitator_repository = facilitator_repository

    async def create(self, facilitator_create: FacilitatorCreate) -> Facilitator:
        return await self._facilitator_repository.create(
            Facilitator(**facilitator_create.model_dump()),
        )

    async def get_by_id(self, facilitator_id: int) -> Facilitator:
        facilitator = await self._facilitator_repository.get_by_id(facilitator_id)

        if facilitator is None:
            raise FacilitatorNotFoundError()

        return facilitator

    async def get_by_user_id(self, user_id: int) -> Facilitator:
        facilitator = await self._facilitator_repository.get_by_user_id(user_id)

        if facilitator is None:
            raise FacilitatorNotFoundError()

        return facilitator
