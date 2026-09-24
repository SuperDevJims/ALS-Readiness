from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field

from app.enums.curriculum import StructureStatus

from .base import BaseEntity


class Lesson(BaseEntity):
    __tablename__ = "lessons"

    module_id: int = Field(foreign_key="modules.id")

    title: str = Field(max_length=255)
    description: str
    order_index: int

    status: StructureStatus | None = Field(
        default=StructureStatus.ACTIVE,
        sa_type=SQLEnum(
            StructureStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="structure_status"
        ),
    )
