from app.models.curriculum import LearningStrand

from .base import BaseRepository


class LearningStrandRepository(BaseRepository[LearningStrand]):

    module = LearningStrand
