from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.enums.user import Gender


class ParticipantIntakeUpsert(BaseModel):
    age: int = Field(ge=15, le=120)
    sex: Gender
    civil_status: str = Field(min_length=1, max_length=50)
    highest_educational_attainment: str = Field(min_length=1, max_length=255)
    als_learning_strands: list[str] = Field(min_length=1)
    als_enrollment_months: int = Field(ge=0, le=1200)
    has_taken_ae_test: bool
    ae_test_attempt_count: int = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_ae_history(self):
        if not self.has_taken_ae_test and self.ae_test_attempt_count != 0:
            raise ValueError("A&E test attempt count must be zero when no prior test was taken.")
        if self.has_taken_ae_test and self.ae_test_attempt_count < 1:
            raise ValueError("A&E test attempt count must be at least one when a prior test was taken.")
        return self


class ParticipantIntakeResponse(ParticipantIntakeUpsert):
    submitted_at: datetime
