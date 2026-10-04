from app.schemas.curriculum import CurriculumResponse
from app.schemas.facilitator_curriculum import FacilitatorCurriculumResponse
from fastapi import APIRouter

from ..deps import (
    CurrentFacilitatorDep,
    CurrentLearnerDep,
    CurriculumServiceDep,
)

router = APIRouter(
    tags=["Curriculum"]
)


@router.get("/curriculum/{strand_id}")
async def get_curriculum(
    strand_id: int,
    current_user: CurrentFacilitatorDep,
    cohort_id: int | None = None,
    service: CurriculumServiceDep = ...,
) -> FacilitatorCurriculumResponse:
    return await service.get_tree(current_user, strand_id, cohort_id)


@router.get("/me/curriculum/{strand_id}")
async def get_my_curriculum(
    strand_id: int,
    current_user: CurrentLearnerDep,
    service: CurriculumServiceDep,
) -> CurriculumResponse:
    return await service.get_tree_with_progress(strand_id, current_user.id)
