from app.schemas.strand_test_attempt import StrandAttemptCreate, StrandAttemptResponse
from fastapi import APIRouter, status

from ..deps import CurrentLearnernDep, StrandAttemptServiceDep

router = APIRouter(
    prefix="/learner/strand-tests/{test_id}/attempts",
    tags=["Strand Test Attempts"],
)


@router.post(
    "",
    response_model=StrandAttemptResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_strand_test_attempt(
    test_id: int,
    attempt_create: StrandAttemptCreate,
    current_user: CurrentLearnernDep,
    attempt_service: StrandAttemptServiceDep,
):
    return await attempt_service.create(
        user_id=current_user.id,
        test_id=test_id,
        attempt_create=attempt_create,
    )
