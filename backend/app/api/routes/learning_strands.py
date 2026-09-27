from app.schemas.curriculum import StrandProgressResponse
from fastapi import APIRouter

from ..deps import CurrentLearnerDep, StrandServiceDep

router = APIRouter(tags=["Learning Strands"])


@router.get("/me/strands")
async def get_my_strands(
    current_user: CurrentLearnerDep,
    service: StrandServiceDep,
) -> list[StrandProgressResponse]:
    return await service.get_progress_list(current_user.id)
