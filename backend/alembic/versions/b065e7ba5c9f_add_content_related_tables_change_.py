"""add content-related tables, change content status enum, and add content progress status enum

Revision ID: b065e7ba5c9f
Revises: 2e7189e345fd
Create Date: 2026-09-24 21:43:28.046078

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b065e7ba5c9f"
down_revision: Union[str, Sequence[str], None] = "2e7189e345fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ------------------------------------------------------------------
    # Replace existing content_status enum
    # ------------------------------------------------------------------

    op.execute(
        "ALTER TYPE content_status RENAME TO content_status_old"
    )

    op.execute(
        """
        CREATE TYPE content_status AS ENUM (
            'active',
            'archived',
            'deleted'
        )
        """
    )

    op.execute(
        """
        DROP TYPE content_status_old
        """
    )

    # ------------------------------------------------------------------
    # Contents
    # ------------------------------------------------------------------

    op.create_table(
        "contents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "file_key",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(),
            nullable=True,
        ),
        sa.Column(
            "type",
            postgresql.ENUM(
                "video",
                "audio",
                "reading",
                name="content_type",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            postgresql.ENUM(
                "active",
                "archived",
                "deleted",
                name="content_status",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ------------------------------------------------------------------
    # Content evaluations
    # ------------------------------------------------------------------

    op.create_table(
        "content_evaluations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column(
            "stimulus_level",
            postgresql.ENUM(
                "low",
                "medium",
                "high",
                name="stimulus_level",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "cognitive_sustainability_rating",
            sa.Float(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["contents.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ------------------------------------------------------------------
    # Cohort content
    # ------------------------------------------------------------------

    op.create_table(
        "cohort_content",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cohort_id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("assigned_by", sa.Integer(), nullable=False),
        sa.Column(
            "assigned_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["cohort_id"],
            ["cohorts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["contents.id"],
        ),
        sa.ForeignKeyConstraint(
            ["assigned_by"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ------------------------------------------------------------------
    # Learner content progress
    # ------------------------------------------------------------------

    # Create the enum explicitly because this is a new enum type.
    progress_status_enum = postgresql.ENUM(
        "not_opened",
        "in_progress",
        "completed",
        name="learner_content_progress_status",
        create_type=False,
    )
    progress_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "learner_content_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("learner_id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            progress_status_enum,
            nullable=False,
        ),
        sa.Column(
            "progress_status",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "last_accessed_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "completed_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["contents.id"],
        ),
        sa.ForeignKeyConstraint(
            ["learner_id"],
            ["learners.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ------------------------------------------------------------------
    # Existing structure changes
    # ------------------------------------------------------------------

    op.alter_column(
        "lessons",
        "description",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )

    op.alter_column(
        "lessons",
        "status",
        existing_type=postgresql.ENUM(
            "active",
            "archived",
            "deleted",
            name="structure_status",
        ),
        nullable=False,
        existing_server_default=sa.text(
            "'active'::structure_status"
        ),
    )

    op.alter_column(
        "modules",
        "description",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )

    op.alter_column(
        "modules",
        "status",
        existing_type=postgresql.ENUM(
            "active",
            "archived",
            "deleted",
            name="structure_status",
        ),
        nullable=False,
        existing_server_default=sa.text(
            "'active'::structure_status"
        ),
    )

    op.alter_column(
        "learning_strands",
        "description",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )

    op.alter_column(
        "learning_strands",
        "status",
        existing_type=postgresql.ENUM(
            "active",
            "archived",
            "deleted",
            name="structure_status",
        ),
        nullable=False,
        existing_server_default=sa.text(
            "'active'::structure_status"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    # ------------------------------------------------------------------
    # Existing structure changes
    # ------------------------------------------------------------------

    op.alter_column(
        "modules",
        "status",
        existing_type=postgresql.ENUM(
            "active",
            "archived",
            "deleted",
            name="structure_status",
        ),
        nullable=True,
        existing_server_default=sa.text(
            "'active'::structure_status"
        ),
    )

    op.alter_column(
        "modules",
        "description",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )

    op.alter_column(
        "lessons",
        "status",
        existing_type=postgresql.ENUM(
            "active",
            "archived",
            "deleted",
            name="structure_status",
        ),
        nullable=True,
        existing_server_default=sa.text(
            "'active'::structure_status"
        ),
    )

    op.alter_column(
        "lessons",
        "description",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )

    op.alter_column(
        "learning_strands",
        "description",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )

    op.alter_column(
        "learning_strands",
        "status",
        existing_type=postgresql.ENUM(
            "active",
            "archived",
            "deleted",
            name="structure_status",
        ),
        nullable=True,
        existing_server_default=sa.text(
            "'active'::structure_status"
        ),
    )

    # ------------------------------------------------------------------
    # Drop content-related tables
    # ------------------------------------------------------------------

    op.drop_table("learner_content_progress")
    op.drop_table("cohort_content")
    op.drop_table("content_evaluations")
    op.drop_table("contents")

    # Drop the new progress enum.
    op.execute(
        "DROP TYPE IF EXISTS learner_content_progress_status"
    )

    # ------------------------------------------------------------------
    # Restore previous content_status enum
    # ------------------------------------------------------------------
    #
    # You still need the OLD values here if you want a working
    # downgrade. Do not invent them.
    #

    op.execute(
        "ALTER TYPE content_status RENAME TO content_status_new"
    )

    op.execute(
        """
        CREATE TYPE content_status AS ENUM (
            'OLD_VALUE_1',
            'OLD_VALUE_2'
        )
        """
    )

    op.execute(
        "DROP TYPE content_status_new"
    )