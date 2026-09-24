"""merge migration heads

Revision ID: 01e062d32564
Revises: 028aa40d4e03, ff411570e867
Create Date: 2026-09-24 10:49:41.428308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01e062d32564'
down_revision: Union[str, Sequence[str], None] = ('028aa40d4e03', 'ff411570e867')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
