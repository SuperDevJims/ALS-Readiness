from app.repositories.curriculum import CurriculumRepository
from app.services.learner import LearnerService


class CurriculumService:
    def __init__(
        self,
        curriculum_repo: CurriculumRepository,
        learner_service: LearnerService,
    ):
        self._curriculum_repo = curriculum_repo
        self._learner_service = learner_service

    async def get_tree(
        self,
        strand_id: int,
        cohort_id: int,
    ):
        pass

    async def get_tree_with_progress(
        self,
        user_id: int,
        strand_id: int,
        cohort_id: int,
    ):
        learner = await self._learner_service.get_by_user_id(user_id)


        
