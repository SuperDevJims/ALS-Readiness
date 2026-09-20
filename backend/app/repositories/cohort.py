from app.models.cohort import Cohort

from .base import BaseRepository


class CohortRepository(BaseRepository[Cohort]):
    model = Cohort
