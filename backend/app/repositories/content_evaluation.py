from app.models.content_evaluation import ContentEvaluation

from .base import BaseRepository


class ContentEvaluationRepository(BaseRepository[ContentEvaluation]):
    model = ContentEvaluation
    