"""restore lessons name column

Revision ID: a966d908fc7a
Revises: 44ef2863336a
Create Date: 2026-09-12 01:07:16.695593

R1 fix: migration 44ef2863336a dropped `lessons.name`, but the `Lesson`
model (app/models/curriculum.py) never stopped declaring it, and
scripts/seed_curriculum.py constructs every Lesson with a `name`. That
migration is the current head and may already be applied in some
environments, so instead of hand-editing it, this migration re-adds the
column on top of it.

The column is added nullable first and backfilled before the NOT NULL
constraint is applied, so this is safe to run both on a fresh database
(no rows, backfill is a no-op) and on a database where 44ef2863336a was
already applied and `lessons` rows exist without a name.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'a966d908fc7a'
down_revision: Union[str, Sequence[str], None] = '44ef2863336a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'lessons',
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    )
    op.execute("UPDATE lessons SET name = '' WHERE name IS NULL")
    op.alter_column('lessons', 'name', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('lessons', 'name')
