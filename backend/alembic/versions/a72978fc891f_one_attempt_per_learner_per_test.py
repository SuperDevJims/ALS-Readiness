"""one attempt per learner per test

Revision ID: a72978fc891f
Revises: a2ab965d28ec
Create Date: 2026-09-19 08:18:11.637141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a72978fc891f'
down_revision: Union[str, Sequence[str], None] = 'a2ab965d28ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Design decision: one attempt per learner per test (FR-M02-12).
    #
    # This fails if either table already holds duplicate (learner_id, test_id)
    # pairs. Check first, and resolve any duplicates before upgrading:
    #   SELECT learner_id, test_id, COUNT(*) FROM strand_test_attempts
    #   GROUP BY 1, 2 HAVING COUNT(*) > 1;
    #   SELECT learner_id, test_id, COUNT(*) FROM lri_test_attempts
    #   GROUP BY 1, 2 HAVING COUNT(*) > 1;
    op.create_unique_constraint(
        'uq_strand_test_attempts_learner_test',
        'strand_test_attempts',
        ['learner_id', 'test_id'],
    )
    op.create_unique_constraint(
        'uq_lri_test_attempts_learner_test',
        'lri_test_attempts',
        ['learner_id', 'test_id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'uq_lri_test_attempts_learner_test', 'lri_test_attempts', type_='unique'
    )
    op.drop_constraint(
        'uq_strand_test_attempts_learner_test', 'strand_test_attempts', type_='unique'
    )
