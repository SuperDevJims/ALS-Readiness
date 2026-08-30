from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field

from app.enums.strand_test import StrandTestType

from .base import BaseEntity


class StrandTest(BaseEntity, table=True):
    __tablename__ = "strand_tests"

    strand_id: int = Field(foreign_key="learning_strands.id")

    title: str = Field(max_length=255)

    type: StrandTestType = Field(
        sa_type=SQLEnum(
            StrandTestType,
            values_callable=lambda enum: [e.value for e in enum],
            
        )
    )


class StrandTestItems(BaseEntity, table=True):
    __tablename__ = "strand_test_items"

    test_id: int = Field(foreign_key="strand_tests.id")

    question_text: str


class StrandTestItemOption(BaseEntity, table=True):
    __tablename__ = "strand_test_item_options"

    item_id: int = Field(foreign_key="strand_test_items.id")

    option_text: str
    is_correct: bool
