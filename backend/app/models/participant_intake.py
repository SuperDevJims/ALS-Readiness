from datetime import datetime

from sqlalchemy import Column, JSON
from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field, SQLModel

from app.enums.user import Gender


class ParticipantIntake(SQLModel, table=True):
    """The once-per-learner background questionnaire submitted before pre-testing."""

    __tablename__ = "participant_intakes"

    user_id: int = Field(primary_key=True, foreign_key="users.id")
    age: int
    sex: Gender = Field(
        sa_type=SQLEnum(
            Gender,
            values_callable=lambda enum: [e.value for e in enum],
        )
    )
    civil_status: str = Field(max_length=50)
    highest_educational_attainment: str = Field(max_length=255)
    als_learning_strands: list[str] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    als_enrollment_months: int
    has_taken_ae_test: bool
    ae_test_attempt_count: int
    submitted_at: datetime | None = Field(default=None)
