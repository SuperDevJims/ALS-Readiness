from pydantic import BaseModel

from app.enums.attempt import AttemptStatus

class LRITestResponse(BaseModel):
    test_id: int
    title: str
    description: str

class LRITestWithAttemptStatus(LRITestResponse):
    attempt_status: AttemptStatus


class LRITestWithAttemptStatusResponse(BaseModel):
    tests: list[LRITestWithAttemptStatus]


class LRITestItemResponse(BaseModel):
    item_id: int
    question_text: str


class LRITestWithItemsResponse(LRITestResponse):
    items: list[LRITestItemResponse]
