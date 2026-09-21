from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.cohort import CohortMemberStatus


class CohortFacilitatorCreate(BaseModel):
    facilitator_id: int


class CohortFacilitatorResponse(BaseModel):
    id: int
    cohort_id: int
    facilitator_id: int
    status: CohortMemberStatus
    assigned_by: int
    assigned_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CohortFacilitatorStatusUpdate(BaseModel):
    status: CohortMemberStatus
