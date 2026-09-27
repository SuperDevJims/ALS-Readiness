from datetime import datetime

from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field, Relationship

from app.enums.content import ContentProgressStatus

from .base import BaseEntity


class LearnerContentProgress(BaseEntity, table=True):
    __tablename__ = "learner_content_progress"

    learner_id: int = Field(foreign_key="learners.id")
    content_id: int = Field(foreign_key="contents.id")

    status: ContentProgressStatus = Field(
        default=ContentProgressStatus.NOT_OPENED,
        sa_type=SQLEnum(
            ContentProgressStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="learner_content_progress_status",
        )
    )

    progress_status: float = Field(default=0)
    last_accessed_at: datetime | None
    completed_at: datetime | None

    content: "Content" = Relationship(back_populates="progress_records")
