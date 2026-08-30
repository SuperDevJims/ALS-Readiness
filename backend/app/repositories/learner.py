from app.models.learner import Learner

from .base import BaseRepository


class LearnerRepository(BaseRepository[Learner]):

    model = Learner
