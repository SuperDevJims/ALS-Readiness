from app.models.strand_test_attempt import StrandTestAttempt

from .base import BaseRepository


class StrandTestAttemptRepository(BaseRepository[StrandTestAttempt]):
    model = StrandTestAttempt
