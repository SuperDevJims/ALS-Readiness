import re
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.enums.cohort import CohortStatus

from .cohort_facilitator import CohortFacilitatorResponse
from .cohort_learner import CohortLearnerResponse
from .user_profile import UserProfileResponse

# Two consecutive years, e.g. "2026-2027". The generated cohort code embeds the
# school year, so a fixed nine-character value also keeps the code within its
# varchar(20) column.
SCHOOL_YEAR_PATTERN = re.compile(r"([0-9]{4})-([0-9]{4})")


class CohortCreate(BaseModel):
    name: str = Field(max_length=100)
    school_year: str
    start_date: date
    end_date: date

    @field_validator("school_year")
    @classmethod
    def validate_school_year(cls, value: str) -> str:
        match = SCHOOL_YEAR_PATTERN.fullmatch(value)
        if match is None or int(match.group(2)) != int(match.group(1)) + 1:
            raise ValueError(
                "School year must be two consecutive years in the form YYYY-YYYY, e.g. 2026-2027."
            )

        return value


class CohortResponse(BaseModel):
    id: int
    name: str
    school_year: str
    start_date: date | None
    end_date: date | None
    code: str | None
    created_by: int
    created_at: datetime
    updated_at: datetime
    status: CohortStatus

    model_config = ConfigDict(from_attributes=True)


class CohortStatusUpdate(BaseModel):
    status: CohortStatus


class CohortListResponse(BaseModel):
    cohorts: list[CohortResponse]


class CohortFacilitatorMemberResponse(CohortFacilitatorResponse):
    profile: UserProfileResponse


class CohortLearnerMemberResponse(CohortLearnerResponse):
    profile: UserProfileResponse


class CohortWithMembersResponse(CohortResponse):
    facilitators: list[CohortFacilitatorMemberResponse]
    learners: list[CohortLearnerMemberResponse]
