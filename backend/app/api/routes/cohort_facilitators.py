from app.schemas.cohort_facilitator import (
    CohortFacilitatorResponse,
    CohortFacilitatorStatusUpdate,
)
from fastapi import APIRouter, Depends

from ..deps import CohortFacilitatorServiceDep, require_admin

router = APIRouter(
    prefix="/cohort-facilitators",
    tags=["Cohort Facilitators"],
    dependencies=[Depends(require_admin)]
)


@router.patch(
    "/{cohort_facilitator_id}/status",
    response_model=CohortFacilitatorResponse | None,
)
async def update_cohort_facilitator_status(
    cohort_facilitator_id: int,
    data: CohortFacilitatorStatusUpdate,
    service: CohortFacilitatorServiceDep,
):
    return await service.update_status(cohort_facilitator_id, data.status)
