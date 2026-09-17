from datetime import datetime

from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field

from app.enums.content import ContentStatus, ContentType

from .base import BaseEntity


class LearningContent(BaseEntity, table=True):
    __tablename__ = "learning_contents"

    strand_id: int = Field(foreign_key="learning_strands.id")

    title: str
    description: str | None

    type: ContentType = Field(
        sa_type=SQLEnum(
            ContentType,
            values_callable=lambda enum: [e.value for e in enum],
            name="content_type",
        )
    )

    status: ContentStatus = Field(
        sa_type=SQLEnum(
            ContentStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="content_status",
        )
    )

    file_path: str
    uploaded_at: datetime
