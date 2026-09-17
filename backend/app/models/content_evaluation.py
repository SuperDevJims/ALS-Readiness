from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field

from app.enums.content import StimulusLevel

from .base import BaseEntity


class ContentEvaluation(BaseEntity, table=True):
    __tablename__ = "content_evaluations"

    content_id: int = Field(foreign_key="learning_contents.id")

    stimulus_level: StimulusLevel = Field(
        sa_type=SQLEnum(
            StimulusLevel,
            values_callable=lambda enum: [e.value for e in enum],
            name="stimulus_level",
        )
    )

    cognitive_sustainability_rating: float = Field(ge=0, le=1)
