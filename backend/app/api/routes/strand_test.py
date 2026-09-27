from app.enums.strand_test import StrandTestType
from app.schemas.strand_test import (
    StrandTestResponse,
    StrandTestWithAttemptStatusResponse,
    StrandTestWithItemsResponse,
)
from fastapi import APIRouter

from ..deps import CurrentLearnerDep, StrandTestServiceDep

router = APIRouter(tags=["Strand Test"])


@router.get("/learner/strand-tests", response_model=StrandTestWithAttemptStatusResponse)
async def get_strand_tests_by_type_with_attempt_status(
    test_type: StrandTestType,
    current_user: CurrentLearnerDep,
    test_service: StrandTestServiceDep,
):
    return await test_service.get_by_type_with_attempt_status(
        user_id=current_user.id, test_type=test_type
    )


@router.get(
    "/learner/strand-tests/{test_id}",
    response_model=StrandTestResponse | StrandTestWithItemsResponse | None,
)
async def get_strand_test_by_id(
    test_id: int,
    include_items: bool = False,
    _: CurrentLearnerDep = ...,
    test_service: StrandTestServiceDep = ...,
):
    return await test_service.get_by_id(test_id, include_items)
