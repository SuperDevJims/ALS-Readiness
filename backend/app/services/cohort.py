from app.repositories.cohort import CohortRepository
from app.schemas.cohort import CohortCreate, CohortResponse
from app.models.cohort import Cohort


class CohortService:
    def __init__(self, cohort_repo: CohortRepository) -> None:
        self._cohort_repo = cohort_repo

    async def create(
        self,
        admin_id: int,
        cohort_create: CohortCreate,
    ) -> CohortResponse:
        school_year = (
            f"{cohort_create.start_date.year}-"
            f"{cohort_create.end_date.year}"
        )

        sequence_number = await self._cohort_repo.get_next_sequence()

        code = f"CBY-{cohort_create.start_date.year}-{sequence_number:02d}"

        cohort = Cohort(
            created_by=admin_id,
            code=code,
            name=cohort_create.name,
            school_year=school_year,
            start_date=cohort_create.start_date,
            end_date=cohort_create.end_date,
        )

        cohort = await self._cohort_repo.create(cohort)

        return CohortResponse.model_validate(cohort)
