from app.schemas.lri_test_attempt import LRITestAttemptCreate, LRITestAttemptResponse
from fastapi import APIRouter, status

from ..deps import CurrentLearnernDep, LRITestAttemptServiceDep

router = APIRouter(tags=["LRI Test Attempt"])


@router.post(
    "/learner/lri-tests/{test_id}/attempts",
    response_model=LRITestAttemptResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_lri_test_attempt(
    test_id: int,
    attempt_create: LRITestAttemptCreate,
    current_user: CurrentLearnernDep,
    attempt_service: LRITestAttemptServiceDep,
):
    return await attempt_service.create(
        test_id=test_id,
        user_id=current_user.id,
        attempt_create=attempt_create,
    )
