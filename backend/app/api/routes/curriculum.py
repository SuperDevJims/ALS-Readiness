from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from ..deps import CurrentLearnernDep, get_current_user

router = APIRouter(
    tags=["Curriculum"]
)


@router.get(
    "/curriculum/{strand_id}",
    dependencies=[Depends(get_current_user)],
)
def get_curriculum(
    strand_id: int,
    cohort_id: int,
    service: None
):
    pass


@router.get(
    "/me/curriculum/{strand_id}",
)
def get_my_curriculum(
    strand_id: int,
    cohort_id: int,
    current_user: CurrentLearnernDep,
    service: None,
):
    pass
