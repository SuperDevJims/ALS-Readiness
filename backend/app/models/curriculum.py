from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field

from app.enums.curriculum import StructureStatus

from .base import BaseEntity, TimestampMixin


class CurriculumStructureBase(BaseEntity, TimestampMixin):
    status: StructureStatus | None = Field(
        default=StructureStatus.ACTIVE,
        sa_type=SQLEnum(
            StructureStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="structure_status"
        ),
    )


class LearningStrand(CurriculumStructureBase, table=True):
    __tablename__ = "learning_strands"

    code: str = Field(max_length=20, unique=True)
    name: str = Field(max_length=255)
    description: str


class Module(CurriculumStructureBase, table=True):
    __tablename__ = "modules"

    strand_id: int = Field(foreign_key="learning_strands.id")

    name: str = Field(max_length=255)
    order_index: int


class Lesson(CurriculumStructureBase, table=True):
    __tablename__ = "lessons"

    module_id: int = Field(foreign_key="modules.id")

    name: str = Field(max_length=255)
    order_index: int
