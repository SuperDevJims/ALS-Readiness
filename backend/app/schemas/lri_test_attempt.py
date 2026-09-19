from datetime import datetime

from pydantic import BaseModel, Field


class LRITestAttemptAnswerCreate(BaseModel):
    # LRI uses a four-point Likert scale: 1 = Strongly Disagree through 4 =
    # Strongly Agree. Keeping the contract here prevents invalid client values
    # from becoming part of a baseline assessment.
    answer_value: int = Field(ge=1, le=4)
    item_id: int


class LRITestAttemptCreate(BaseModel):
    answers: list[LRITestAttemptAnswerCreate]


class LRITestAttemptResponse(BaseModel):
    attempt_id: int
    status: str


class LRITestAttemptResultResponse(BaseModel):
    attempt_id: int
    test_id: int
    lri_score: float
    submitted_at: datetime | None
