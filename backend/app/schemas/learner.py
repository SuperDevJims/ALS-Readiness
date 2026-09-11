from pydantic import BaseModel


class LearnerCreate(BaseModel):
    user_id: int
