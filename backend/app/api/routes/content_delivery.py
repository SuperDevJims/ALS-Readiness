from fastapi import APIRouter

router = APIRouter(
    prefix="/content-deliveries",
    tags=["Content Deliveries"]
)


@router.get("/")
def get_readiness_matched_content():
    """
    Retrieved learning content matched to the learner's readiness level.
    """
