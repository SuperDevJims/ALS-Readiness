from datetime import datetime

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import func
from sqlmodel import Field

from app.enums.content import ContentStatus, ContentType, ContentVisibility

from .base import BaseEntity


class Content(BaseEntity, table=True):
    __tablename__ = "contents"

    lesson_id: int = Field(foreign_key="lessons.id")

    file_key: str = Field(max_length=255)
    title: str = Field(max_length=255)
    description: str | None

    type: ContentType = Field(
        sa_type=SQLEnum(
            ContentType,
            values_callable=lambda enum: [e.value for e in enum],
            name="content_type",
        )
    )

    status: ContentStatus = Field(
        default=ContentStatus.ACTIVE,
        sa_type=SQLEnum(
            ContentStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="content_status",
        ),
    )

    visibility: ContentVisibility = Field(
        default=ContentVisibility.PRIVATE,
        sa_type=SQLEnum(
            ContentVisibility,
            values_callable=lambda enum: [e.value for e in enum],
            name="content_visibility",
        ),
    )

    uploaded_by: int | None = Field(
        default=None,
        foreign_key="facilitators.id",
    )

    uploaded_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now()},
    )
