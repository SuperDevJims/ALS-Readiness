"""Make Cohort Code Nullable

Revision ID: 028aa40d4e03
Revises: d92cf08e73fd
Create Date: 2026-09-20 14:11:29.581777

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "028aa40d4e03"
down_revision: Union[str, Sequence[str], None] = "d92cf08e73fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "cohorts",
        "code",
        existing_type=sa.VARCHAR(length=20),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "cohorts",
        "code",
        existing_type=sa.VARCHAR(length=20),
        nullable=False,
    )