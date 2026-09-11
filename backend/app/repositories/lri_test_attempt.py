from app.models.lri_test_attempt import LRITestAttempt

from .base import BaseRepository


class LRITestAttemptRepository(BaseRepository[LRITestAttempt]):
    model = LRITestAttempt
    