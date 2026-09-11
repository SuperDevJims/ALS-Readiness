from pydantic import BaseModel


class StrandAttemptAnswerCreate(BaseModel):
    item_id: int
    option_id: int


class StrandAttemptCreate(BaseModel):
    answers: list[StrandAttemptAnswerCreate]


class StrandAttemptResponse(BaseModel):
    attempt_id: int
    status: str
