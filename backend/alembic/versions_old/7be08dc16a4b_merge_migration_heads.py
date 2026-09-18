"""merge migration heads

Revision ID: 7be08dc16a4b
Revises: 35bba06153c7, d2f8b1234cde
Create Date: 2026-09-18 08:23:55.112421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7be08dc16a4b'
down_revision: Union[str, Sequence[str], None] = ('35bba06153c7', 'd2f8b1234cde')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
