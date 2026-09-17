from sqlmodel import Field

from .base import BaseEntity


class LRITest(BaseEntity, table=True): 
    __tablename__ = "lri_tests"

    title: str = Field(max_length=100)
    description: str
    image_url: str = Field(max_length=2048)


class LRITestItem(BaseEntity, table=True):
    __tablename__ = "lri_test_items"

    test_id: int = Field(foreign_key="lri_tests.id")

    question_text: str
