from datetime import datetime

from sqlalchemy import func
from sqlmodel import Field

from .base import BaseEntity


class StrandTestAttempt(BaseEntity, table=True):
    __tablename__ = "strand_test_attempts"

    test_id: int = Field(foreign_key="strand_tests.id")
    learner_id: int = Field(foreign_key="learners.id")

    total_score: int

    taken_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )


class StrandTestAttemptAnswer(BaseEntity, table=True):
    __tablename__ = "strand_test_attempt_answers"

    attempt_id: int = Field(foreign_key="strand_test_attempts.id")
    item_id: int = Field(foreign_key="strand_test_items.id")
    option_id: int = Field(foreign_key="strand_test_item_options.id")

    is_correct: bool
