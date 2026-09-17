"""add image URLs to learner assessments

Revision ID: d2f8b1234cde
Revises: a966d908fc7a, c18e4f9a7b2d
Create Date: 2026-09-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d2f8b1234cde"
down_revision: Union[str, Sequence[str], None] = ("a966d908fc7a", "c18e4f9a7b2d")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_TEST_IMAGE_URL = (
    "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?"
    "auto=format&fit=crop&w=1200&q=80"
)


def upgrade() -> None:
    for table_name in ("lri_tests", "strand_tests"):
        op.add_column(
            table_name,
            sa.Column(
                "image_url",
                sa.String(length=2048),
                nullable=False,
                server_default=DEFAULT_TEST_IMAGE_URL,
            ),
        )
        op.alter_column(table_name, "image_url", server_default=None)


def downgrade() -> None:
    op.drop_column("strand_tests", "image_url")
    op.drop_column("lri_tests", "image_url")
