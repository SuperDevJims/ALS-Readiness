from datetime import datetime

from pydantic import BaseModel


class StrandAttemptAnswerCreate(BaseModel):
    item_id: int
    option_id: int


class StrandAttemptCreate(BaseModel):
    answers: list[StrandAttemptAnswerCreate]


class StrandAttemptResponse(BaseModel):
    attempt_id: int
    status: str


class StrandAttemptResultResponse(BaseModel):
    attempt_id: int
    test_id: int
    total_score: int  # raw count of correct answers
    item_count: int  # items in the test at submission time
    mps: float  # Mean Percentage Score: total_score / item_count * 100, 2 dp
    taken_at: datetime | None
