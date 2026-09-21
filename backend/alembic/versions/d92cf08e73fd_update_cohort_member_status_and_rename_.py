"""Update cohort member status and rename cohort members

Revision ID: d92cf08e73fd
Revises: a72978fc891f
Create Date: 2026-09-20 13:21:11.342286
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d92cf08e73fd"
down_revision: Union[str, Sequence[str], None] = "a72978fc891f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the existing table instead of dropping and recreating it.
    op.rename_table("cohort_members", "cohort_learners")

    # Change cohort_facilitators.status to use the shared
    # cohort_member_status enum.
    op.execute("""
        ALTER TABLE cohort_facilitators
        ALTER COLUMN status TYPE cohort_member_status
        USING status::text::cohort_member_status
    """)

    # The old facilitator-specific enum is no longer needed.
    op.execute("DROP TYPE cohort_facilitator_status")


def downgrade() -> None:
    # Recreate the old facilitator-specific enum.
    op.execute("""
        CREATE TYPE cohort_facilitator_status AS ENUM (
            'active',
            'ended',
            'removed'
        )
    """)

    # Change facilitator status back to the old enum.
    op.execute("""
        ALTER TABLE cohort_facilitators
        ALTER COLUMN status TYPE cohort_facilitator_status
        USING status::text::cohort_facilitator_status
    """)

    # Rename the table back.
    op.rename_table("cohort_learners", "cohort_members")
