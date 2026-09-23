"""add super admin and must change password to users

Revision ID: ff411570e867
Revises: a72978fc891f
Create Date: 2026-09-21 11:39:42.815708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff411570e867'
down_revision: Union[str, Sequence[str], None] = 'a72978fc891f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # server_default backfills existing rows so NOT NULL can be applied.
    op.add_column('users', sa.Column('is_super_admin', sa.Boolean(), server_default=sa.false(), nullable=False))
    op.add_column('users', sa.Column('must_change_password', sa.Boolean(), server_default=sa.false(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'must_change_password')
    op.drop_column('users', 'is_super_admin')
