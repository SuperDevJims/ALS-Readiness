from app.schemas.strand_attempt import StrandAttemptCreate, StrandAttemptResponse
from fastapi import APIRouter

router = APIRouter(
    prefix="/strand-tests/{test_id}/attempts",
    tags=["Strand Test Attempts"],
)


@router.post("", response_model=StrandAttemptResponse)
def create_attempt(test_id: int, attempt: StrandAttemptCreate):
    pass
