from app.enums.cohort import CohortStatus
from app.schemas.cohort import (
    CohortCreate,
    CohortListResponse,
    CohortResponse,
    CohortStatusUpdate,
)
from app.schemas.cohort_facilitator import (
    CohortFacilitatorCreate,
    CohortFacilitatorResponse,
)
from app.schemas.cohort_learner import CohortLearnerCreate, CohortLearnerResponse
from fastapi import APIRouter, Depends, status

from ..deps import CohortServiceDep, RequireAdminDep, require_admin

router = APIRouter(
    prefix="/cohorts", 
    tags=["Cohorts"],
)


# ================ Admin-only ================ 

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CohortResponse,
    dependencies=[Depends(require_admin)],
)
async def create_cohort(
    cohort_create: CohortCreate,
    current_user: RequireAdminDep,
    cohort_service: CohortServiceDep,
):
    res = await cohort_service.create(current_user.id, cohort_create)
    return CohortResponse.model_validate(res)


@router.get(
    "",
    response_model=CohortListResponse,
    dependencies=[Depends(require_admin)],
)
async def get_cohorts(
    status: CohortStatus | None = None,
    cohort_service: CohortServiceDep = ...,
):
    cohorts = await cohort_service.get_list(status)
    return CohortListResponse(
        cohorts=[CohortResponse.model_validate(cohort) for cohort in cohorts]
    )


@router.patch(
    "/{cohort_id}/status",
    response_model=CohortResponse,
    dependencies=[Depends(require_admin)],
)
async def update_cohort_status(
    cohort_id: int,
    cohort_update: CohortStatusUpdate,
    cohort_service: CohortServiceDep,
):
    cohort = await cohort_service.update_status(cohort_id, cohort_update.status)
    return CohortResponse.model_validate(cohort)


@router.post(
    "/{cohort_id}/learners",
    status_code=status.HTTP_201_CREATED,
    response_model=CohortLearnerResponse,
    dependencies=[Depends(require_admin)],
)
async def assign_learner_to_cohort(
    cohort_id: int,
    cohort_learner_create: CohortLearnerCreate,
    current_user: RequireAdminDep,
    cohort_service: CohortServiceDep,
):
    cohort_learner = await cohort_service.assign_learner(
        admin_id=current_user.id,
        cohort_id=cohort_id,
        learner_id=cohort_learner_create.learner_id
    )
    return CohortLearnerResponse.model_validate(cohort_learner)


@router.post(
    "/{cohort_id}/facilitators",
    status_code=status.HTTP_201_CREATED,
    response_model=CohortFacilitatorResponse,
    dependencies=[Depends(require_admin)],
)
async def assign_facilitator_to_cohort(
    cohort_id: int,
    cohort_facilitator_create: CohortFacilitatorCreate,
    current_user: RequireAdminDep,
    cohort_service: CohortServiceDep,
):
    result = await cohort_service.assign_facilitator(
        admin_id=current_user.id,
        cohort_id=cohort_id,
        facilitator_id=cohort_facilitator_create.facilitator_id,
    )

    return CohortFacilitatorResponse.model_validate(result)


# ================ Shared ================ 

@router.get("/{cohort_id}/members")
async def get_cohort_with_members(cohort_id: int, cohort_service: CohortServiceDep):
    return await cohort_service.get_cohort_with_members(cohort_id)
