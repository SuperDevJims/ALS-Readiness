from datetime import date, datetime

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Index, UniqueConstraint, func, text
from sqlmodel import Field

from app.enums.cohort import *

from .base import BaseEntity, TimestampMixin


class Cohort(BaseEntity, TimestampMixin, table=True):
    __tablename__ = "cohorts"

    created_by: int = Field(foreign_key="users.id")

    code: str = Field(max_length=20, unique=True)
    name: str = Field(max_length=100)
    school_year: str = Field(max_length=20)

    status: CohortStatus = Field(
        default=CohortStatus.UPCOMING,
        sa_type=SQLEnum(
            CohortStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="cohort_status",
        ),
    )

    start_date: date | None = Field(default=None)
    end_date: date | None = Field(default=None)


class CohortLearners(BaseEntity, table=True):
    __tablename__ = "cohort_learners"

    cohort_id: int = Field(foreign_key="cohorts.id")
    learner_id: int = Field(foreign_key="learners.id")

    status: CohortMemberStatus = Field(
        default=CohortMemberStatus.ACTIVE,
        sa_type=SQLEnum(
            CohortMemberStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="cohort_member_status",
        ),
    )

    assigned_by: int = Field(foreign_key="users.id")
    assigned_at: datetime = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now()},
    )
    completed_at: datetime | None = Field(default=None)

    __table_args__ = (
        Index(
            "one_active_cohort_per_learner",
            "learner_id",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
    )


class CohortFacilitators(BaseEntity, table=True):
    __tablename__ = "cohort_facilitators"

    cohort_id: int = Field(foreign_key="cohorts.id")
    facilitator_id: int = Field(foreign_key="facilitators.id")

    status: CohortMemberStatus = Field(
        default=CohortMemberStatus.ACTIVE,
        sa_type=SQLEnum(
            CohortMemberStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="cohort_member_status",
        ),
    )

    assigned_by: int = Field(foreign_key="users.id")
    assigned_at: datetime = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now()},
    )
    ended_at: datetime | None = Field(default=None)

    __table_args__ = (
        UniqueConstraint(
            "cohort_id",
            "facilitator_id",
            name="uq_cohort_facilitators_cohort_facilitator",
        ),
    )
