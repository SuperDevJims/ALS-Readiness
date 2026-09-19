from datetime import datetime

from sqlalchemy import UniqueConstraint, func
from sqlmodel import Field

from .base import BaseEntity


class StrandTestAttempt(BaseEntity, table=True):
    __tablename__ = "strand_test_attempts"

    test_id: int = Field(foreign_key="strand_tests.id")
    learner_id: int = Field(foreign_key="learners.id")

    # Raw count of correct answers.
    total_score: int
    # Number of items in the test when this attempt was submitted. Together with
    # total_score it makes the MPS derivable: total_score / item_count * 100.
    item_count: int

    taken_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )

    # One attempt per learner per test.
    __table_args__ = (
        UniqueConstraint(
            "learner_id", "test_id", name="uq_strand_test_attempts_learner_test"
        ),
    )


class StrandTestAttemptAnswer(BaseEntity, table=True):
    __tablename__ = "strand_test_attempt_answers"

    attempt_id: int = Field(foreign_key="strand_test_attempts.id")
    item_id: int = Field(foreign_key="strand_test_items.id")
    option_id: int = Field(foreign_key="strand_test_item_options.id")

    is_correct: bool
