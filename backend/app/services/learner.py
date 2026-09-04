from app.core.exceptions import LearnerNotFoundError
from app.models.learner import Learner
from app.repositories.learner import LearnerRepository
from app.schemas.learner import LearnerCreate


class LearnerService:
    def __init__(self, learner_repository: LearnerRepository):
        self._learner_repository = learner_repository

    async def create(self, learner_create: LearnerCreate) -> Learner:
        return await self._learner_repository.create(
            Learner(**learner_create.model_dump()),
        )

    async def get_by_id(self, learner_id: int) -> Learner:
        learner = self._learner_repository.get_by_id(learner_id)

        if learner is None:
            raise LearnerNotFoundError()

        return learner

    async def get_by_user_id(self, user_id: int) -> Learner:
        learner = await self._learner_repository.get_by_user_id(user_id)

        if learner is None:
            raise LearnerNotFoundError()

        return learner
