from pydantic import BaseModel, ConfigDict

from app.enums.attempt import AttemptStatus
from app.enums.strand_test import StrandTestType


class StrandTestWithAttemptStatus(BaseModel):
    test_id: int
    title: str
    image_url: str | None = None
    strand_id: int
    strand_code: str
    strand_name: str
    attempt_status: AttemptStatus


class StrandTestWithAttemptStatusResponse(BaseModel):
    tests: list[StrandTestWithAttemptStatus]


class StrandTestItemOptionResponse(BaseModel):
    option_id: int
    option_text: str


class StrandTestItemWithOptionsResponse(BaseModel):
    item_id: int
    question_text: str
    options: list[StrandTestItemOptionResponse]
    asset_url: str | None


class StrandTestResponse(BaseModel):
    test_id: int
    strand_id: int
    title: str
    type:  StrandTestType

    model_config = ConfigDict(from_attributes=True)


class StrandTestWithItemsResponse(StrandTestResponse):
    items: list[StrandTestItemWithOptionsResponse]
