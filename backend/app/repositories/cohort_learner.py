from sqlalchemy import func, select

from app.models.cohort import CohortLearner
from app.models.learner import Learner
from app.models.user import User
from app.models.user_profile import UserProfile
from app.enums.cohort import CohortMemberStatus

from .base import BaseRepository


class CohortLearnerRepository(BaseRepository[CohortLearner]):
    model = CohortLearner

    async def get_by_cohort_id_and_learner_id(
        self,
        cohort_id: int,
        learner_id: int,
    ) -> CohortLearner | None:
        statement = select(CohortLearner).where(
            CohortLearner.cohort_id == cohort_id,
            CohortLearner.learner_id == learner_id,
        )
        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_all_by_cohort_id_with_profile(
        self, 
        cohort_id: int
    ) -> list[tuple[CohortLearner, UserProfile]]:
        statement = (
            select(CohortLearner, UserProfile)
            .join(Learner, Learner.id == CohortLearner.learner_id)
            .join(User, User.id == Learner.user_id)
            .join(UserProfile, UserProfile.user_id == User.id)
            .where(CohortLearner.cohort_id == cohort_id)
        )
        result = await self._session.execute(statement)
        return result.all()

    async def get_active_by_learner_id(self, learner_id: int) -> CohortLearner | None:
        statement = (
            select(CohortLearner)
            .where(
                CohortLearner.learner_id == learner_id, 
                CohortLearner.status == CohortMemberStatus.ACTIVE,
            )
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def exists_in_cohorts(self, learner_id: int, cohort_ids: list[int]) -> bool:
        """Whether the learner has a membership, active or ended, in any of the cohorts."""
        if not cohort_ids:
            return False

        statement = (
            select(CohortLearner.id)
            .where(
                CohortLearner.learner_id == learner_id,
                CohortLearner.cohort_id.in_(cohort_ids),
            )
            .limit(1)
        )
        result = await self._session.execute(statement)
        return result.first() is not None

    async def count_active_by_cohort_ids(self, cohort_ids: list[int]) -> dict[int, int]:
        """Active membership count per cohort, in one query. Cohorts with none are absent."""
        if not cohort_ids:
            return {}

        statement = (
            select(CohortLearner.cohort_id, func.count(CohortLearner.id))
            .where(
                CohortLearner.cohort_id.in_(cohort_ids),
                CohortLearner.status == CohortMemberStatus.ACTIVE,
            )
            .group_by(CohortLearner.cohort_id)
        )
        result = await self._session.execute(statement)
        return {cohort_id: count for cohort_id, count in result.all()}

    async def get_roster_by_cohort_id(
        self,
        cohort_id: int,
    ) -> list[tuple[CohortLearner, str | None, str | None, str | None]]:
        """Every membership of the cohort (active and ended) with the learner's
        id number and name only, ordered by last name then first name.

        Rows are (membership, id_no, first_name, last_name).
        """
        statement = (
            select(CohortLearner, User.id_no, UserProfile.first_name, UserProfile.last_name)
            .join(Learner, Learner.id == CohortLearner.learner_id)
            .join(User, User.id == Learner.user_id)
            .outerjoin(UserProfile, UserProfile.user_id == User.id)
            .where(CohortLearner.cohort_id == cohort_id)
            .order_by(UserProfile.last_name, UserProfile.first_name, CohortLearner.id)
        )
        result = await self._session.execute(statement)
        return result.all()
