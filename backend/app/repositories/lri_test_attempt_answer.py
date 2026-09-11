from app.models.lri_test_attempt import LRITestAttemptAnswer

from .base import BaseRepository


class LRITestAttemptAnswerRepository(BaseRepository[LRITestAttemptAnswer]):
    model = LRITestAttemptAnswer
