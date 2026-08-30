from sqlalchemy import select

from app.models.curriculum import LearningStrand
from app.models.strand_test import StrandTest
from app.models.strand_test_attempt import StrandTestAttempt

from .base import BaseRepository


class StrandTestRepository(BaseRepository[StrandTest]):

    model = StrandTest

    def get_with_attempt_status(learner_id: int):
        statement = (
            select(StrandTest, LearningStrand, StrandTestAttempt)
            .join(
                LearningStrand,
                LearningStrand.id == StrandTest.strand_id
            )
            .outerjoin(
                StrandTestAttempt,
                (StrandTestAttempt.test_id == StrandTest.id)
                & (StrandTestAttempt.learner_id == learner_id)
            )
        )
