from app.schemas.cohort_learner import CohortLearnerResponse, CohortLearnerStatusUpdate
from fastapi import APIRouter, Depends

from ..deps import CohortLearnerServiceDep, require_admin

router = APIRouter(
    prefix="/cohort-learners",
    tags=["Cohort Learners"],
    dependencies=[Depends(require_admin)],
)


@router.patch(
    "/{cohort_learner_id}/status",
    response_model=CohortLearnerResponse | None,
)
async def update_cohort_learner_status(
    cohort_learner_id: int,
    data: CohortLearnerStatusUpdate,
    service: CohortLearnerServiceDep,
):
    return await service.update_status(cohort_learner_id, data.status)
