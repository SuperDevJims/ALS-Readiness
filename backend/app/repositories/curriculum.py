from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cohort import Cohort
from app.models.cohort_content import CohortContent
from app.models.content import Content
from app.models.content_evaluation import ContentEvaluation
from app.models.learner_content_progress import LearnerContentProgress
from app.models.learning_strand import LearningStrand
from app.models.lesson import Lesson
from app.models.module import Module


class CurriculumRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_with_progress(
        self,
        learner_id: int,
        strand_id: int,
        cohort_id: int,
    ) -> tuple[
        LearningStrand,
        Cohort,
        Module,
        Lesson,
        Content,
        ContentEvaluation,
        LearnerContentProgress
    ]:
        pass
