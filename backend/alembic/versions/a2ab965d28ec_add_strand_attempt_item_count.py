"""add strand attempt item count

Revision ID: a2ab965d28ec
Revises: 67d662c2aef6
Create Date: 2026-09-18 23:59:35.033168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2ab965d28ec'
down_revision: Union[str, Sequence[str], None] = '67d662c2aef6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Snapshot of the test's item count at submission time, so a percentage
    # (MPS) is derivable from an attempt row alone: total_score / item_count.
    # Added nullable first so existing attempts can be backfilled.
    op.add_column(
        'strand_test_attempts',
        sa.Column('item_count', sa.Integer(), nullable=True),
    )

    # Backfill from each attempt's test's current item count.
    op.execute(
        """
        UPDATE strand_test_attempts AS a
        SET item_count = (
            SELECT COUNT(*)
            FROM strand_test_items AS i
            WHERE i.test_id = a.test_id
        )
        """
    )

    op.alter_column('strand_test_attempts', 'item_count', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('strand_test_attempts', 'item_count')
