from fastapi import APIRouter, status

from app.schemas.participant_intake import ParticipantIntakeResponse, ParticipantIntakeUpsert

from ..deps import CurrentLearnernDep, ParticipantIntakeServiceDep

router = APIRouter(prefix="/learner/participant-intake", tags=["Participant Intake"])


@router.get("", response_model=ParticipantIntakeResponse | None)
async def get_participant_intake(
    current_user: CurrentLearnernDep,
    intake_service: ParticipantIntakeServiceDep,
):
    return await intake_service.get_by_user_id(current_user.id)


@router.post("", response_model=ParticipantIntakeResponse, status_code=status.HTTP_201_CREATED)
async def submit_participant_intake(
    intake: ParticipantIntakeUpsert,
    current_user: CurrentLearnernDep,
    intake_service: ParticipantIntakeServiceDep,
):
    return await intake_service.upsert(current_user.id, intake)


@router.put("", response_model=ParticipantIntakeResponse)
async def update_participant_intake(
    intake: ParticipantIntakeUpsert,
    current_user: CurrentLearnernDep,
    intake_service: ParticipantIntakeServiceDep,
):
    return await intake_service.upsert(current_user.id, intake)
