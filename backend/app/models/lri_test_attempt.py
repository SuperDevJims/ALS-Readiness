from datetime import datetime

from sqlalchemy import func
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


class LRITestAttemptAnswer(BaseEntity, table=True):
    __tablename__ = "lri_test_attempt_answers"

    item_id: int = Field(foreign_key="lri_test_items.id")
    attempt_id: int = Field(foreign_key="lri_test_attempts.id")

    answer_value: int
