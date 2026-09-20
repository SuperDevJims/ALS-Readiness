from datetime import date, datetime

from pydantic import BaseModel, Field

from app.enums.cohort import CohortStatus


class CohortCreate(BaseModel):
    name: str = Field(max_length=100)
    start_date: date
    end_date: date


class CohortResponse(BaseModel):
    name: str
    start_date: date
    end_date: date
    code: str
    created_by: int
    created_at: datetime
    updated_at: datetime


class CohortStatusUpdate(BaseModel):
    status: CohortStatus
