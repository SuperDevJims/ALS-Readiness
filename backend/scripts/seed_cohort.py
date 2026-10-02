# This script seeds a single cohort with a facilitator assigned to it, for
# local development/testing purposes. Learners are left unassigned when run
# standalone so the facilitator can assign them.
# Assumes an admin and a facilitator already exist.
# Run 'uv run python -m scripts.seed_cohort'.

import asyncio
import sys
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.enums.user import UserRole
from app.models.cohort import Cohort, CohortFacilitator, CohortLearner
from app.models.facilitator import Facilitator
from app.models.user import User
from app.repositories.cohort import CohortRepository
from app.repositories.cohort_facilitator import CohortFacilitatorRepository
from app.repositories.cohort_learner import CohortLearnerRepository

COHORT_DATA = {
    "code": "COH-2026-01",
    "name": "Cohort 1 - School Year 2026-2027",
    "school_year": "2026-2027",
    "start_date": date(2026, 8, 1),
    "end_date": date(2027, 5, 31),
}


async def create_cohort_with_members(session: AsyncSession, learner_id: int | None, facilitator_id: int, admin_user_id: int) -> None:
    cohort_repo = CohortRepository(session)
    cohort_learner_repo = CohortLearnerRepository(session)
    cohort_facilitator_repo = CohortFacilitatorRepository(session)

    cohort = await cohort_repo.create(
        Cohort(
            created_by=admin_user_id,
            code=COHORT_DATA["code"],
            name=COHORT_DATA["name"],
            school_year=COHORT_DATA["school_year"],
            start_date=COHORT_DATA["start_date"],
            end_date=COHORT_DATA["end_date"],
        )
    )
    print(f"Cohort created - code: {cohort.code}, id: {cohort.id}")

    if learner_id is not None:
        cohort_learner = await cohort_learner_repo.create(
            CohortLearner(
                cohort_id=cohort.id,
                learner_id=learner_id,
                assigned_by=admin_user_id,
            )
        )
        print(
            f"  Learner assigned - learner_id: {cohort_learner.learner_id}, "
            f"cohort_id: {cohort_learner.cohort_id}"
        )

    cohort_facilitator = await cohort_facilitator_repo.create(
        CohortFacilitator(
            cohort_id=cohort.id,
            facilitator_id=facilitator_id,
            assigned_by=admin_user_id,
        )
    )
    print(
        f"  Facilitator assigned - facilitator_id: {cohort_facilitator.facilitator_id}, "
        f"cohort_id: {cohort_facilitator.cohort_id}"
    )


async def main() -> None:
    async with AsyncSessionLocal() as session, session.begin():
        admin_user_id = await session.scalar(
            select(User.id).where(User.role == UserRole.ADMIN).order_by(User.id)
        )
        facilitator_id = await session.scalar(select(Facilitator.id).order_by(Facilitator.id))
        if admin_user_id is None or facilitator_id is None:
            raise SystemExit("Seed an admin and a facilitator first.")

        await create_cohort_with_members(session, None, facilitator_id, admin_user_id)


if __name__ == "__main__":
    asyncio.run(main())
