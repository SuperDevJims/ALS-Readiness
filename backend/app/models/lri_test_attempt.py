from datetime import datetime

from sqlalchemy import UniqueConstraint, func
from sqlmodel import Field

from .base import BaseEntity


class LRITestAttempt(BaseEntity, table=True):
    __tablename__ = "lri_test_attempts"

    test_id: int = Field(foreign_key="lri_tests.id")
    learner_id: int = Field(foreign_key="learners.id")

    lri_score: float

    submitted_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": func.now()
        },
    )

    # One attempt per learner per test.
    __table_args__ = (
        UniqueConstraint(
            "learner_id", "test_id", name="uq_lri_test_attempts_learner_test"
        ),
    )


class LRITestAttemptAnswer(BaseEntity, table=True):
    __tablename__ = "lri_test_attempt_answers"

    item_id: int = Field(foreign_key="lri_test_items.id")
    attempt_id: int = Field(foreign_key="lri_test_attempts.id")

    answer_value: int
