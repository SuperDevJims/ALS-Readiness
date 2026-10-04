from app.schemas.facilitator_cohort import (
    FacilitatorCohortDetailResponse,
    FacilitatorCohortListResponse,
    FacilitatorSchoolYearsResponse,
)
from fastapi import APIRouter, Depends

from ..deps import (
    CurrentFacilitatorDep,
    FacilitatorCohortServiceDep,
    get_current_facilitator,
)

router = APIRouter(
    prefix="/facilitator",
    tags=["Facilitator"],
    dependencies=[Depends(get_current_facilitator)],
)


@router.get("/school-years", response_model=FacilitatorSchoolYearsResponse)
async def get_my_school_years(
    current_user: CurrentFacilitatorDep,
    service: FacilitatorCohortServiceDep,
):
    return await service.get_school_years(current_user)


@router.get("/cohorts", response_model=FacilitatorCohortListResponse)
async def get_my_cohorts(
    current_user: CurrentFacilitatorDep,
    service: FacilitatorCohortServiceDep,
    school_year: str | None = None,
):
    return await service.get_cohorts(current_user, school_year)


@router.get("/cohorts/{cohort_id}", response_model=FacilitatorCohortDetailResponse)
async def get_my_cohort(
    cohort_id: int,
    current_user: CurrentFacilitatorDep,
    service: FacilitatorCohortServiceDep,
):
    return await service.get_cohort_detail(current_user, cohort_id)
