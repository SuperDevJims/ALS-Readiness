from app.models.strand_test_attempt import StrandTestAttemptAnswer

from .base import BaseRepository


class StrandTestAttemptAnswerRepository(BaseRepository[StrandTestAttemptAnswer]):
    model = StrandTestAttemptAnswer
