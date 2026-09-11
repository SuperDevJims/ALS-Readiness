from pydantic import BaseModel


class LRITestAttemptAnswerCreate(BaseModel):
    answer_value: int
    item_id: int


class LRITestAttemptCreate(BaseModel):
    answers: list[LRITestAttemptAnswerCreate]


class LRITestAttemptResponse(BaseModel):
    attempt_id: int
    status: str
