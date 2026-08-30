from app.schemas.strand_test_attempt import StrandAttemptCreate, StrandAttemptResponse
from fastapi import APIRouter

from ..deps import CurrentLearnernDep, StrandTestAttemptService

router = APIRouter(
    prefix="/strand-tests/{test_id}/attempts",
    tags=["Strand Test Attempts"],
)


@router.post("", response_model=StrandAttemptResponse)
async def create_attempt(
    test_id: int,
    attempt_create: StrandAttemptCreate,
    current_user: CurrentLearnernDep,
    attempt_service: StrandTestAttemptService,
):
    await attempt_service.create(
        user_id=current_user.id,
        test_id=test_id,
        attempt_create=attempt_create,
    )
