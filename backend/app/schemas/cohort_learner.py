from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.cohort import CohortMemberStatus


class CohortLearnerCreate(BaseModel):
    learner_id: int


class CohortLearnerResponse(BaseModel):
    id: int
    cohort_id: int
    learner_id: int
    status: CohortMemberStatus
    assigned_by: int
    assigned_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CohortLearnerStatusUpdate(BaseModel):
    status: CohortMemberStatus
