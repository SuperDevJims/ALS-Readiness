from fastapi import APIRouter, Depends

from ..deps import get_current_user

router = APIRouter(
    prefix="/curriculum",
    tags=["Curriculum"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/{strand}")
def get_curriculum_for_strand_and_cohort(cohort_id: int):
    pass