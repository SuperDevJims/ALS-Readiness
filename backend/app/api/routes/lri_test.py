from app.schemas.lri_test import (
    LRITestWithAttemptStatusResponse,
    LRITestWithItemsResponse,
)
from fastapi import APIRouter

from ..deps import CurrentLearnernDep, LRITestServiceDep

router = APIRouter(tags=["LRI Test"])


@router.get("/learner/lri-tests", response_model=LRITestWithAttemptStatusResponse)
async def get_lri_tests_with_attempt_status(current_user: CurrentLearnernDep, test_service: LRITestServiceDep):
    return await test_service.get_with_attempt_status(current_user.id)


@router.get("/learner/lri-tests/{test_id}", response_model=LRITestWithItemsResponse)
async def get_lri_test_with_items(
    test_id: int,
    _: CurrentLearnernDep,
    test_service: LRITestServiceDep,
):
    return await test_service.get_by_id_with_items(test_id)
