"""add participant intakes

Revision ID: c18e4f9a7b2d
Revises: 44ef2863336a
Create Date: 2026-09-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c18e4f9a7b2d"
down_revision: Union[str, Sequence[str], None] = "44ef2863336a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "participant_intakes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("sex", sa.Enum("male", "female", "other", name="gender"), nullable=False),
        sa.Column("civil_status", sa.String(length=50), nullable=False),
        sa.Column("highest_educational_attainment", sa.String(length=255), nullable=False),
        sa.Column("als_learning_strands", sa.JSON(), nullable=False),
        sa.Column("als_enrollment_months", sa.Integer(), nullable=False),
        sa.Column("has_taken_ae_test", sa.Boolean(), nullable=False),
        sa.Column("ae_test_attempt_count", sa.Integer(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("participant_intakes")
