from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field

from app.enums.curriculum import StructureStatus

from .base import BaseEntity
    

class LearningStrand(BaseEntity, table=True):
    __tablename__ = "learning_strands"

    code: str = Field(max_length=20, unique=True)
    name: str = Field(max_length=255)
    description: str

    status: StructureStatus | None = Field(
            default=StructureStatus.ACTIVE,
            sa_type=SQLEnum(
                StructureStatus,
                values_callable=lambda enum: [e.value for e in enum],
                name="structure_status"
            ),
        )
