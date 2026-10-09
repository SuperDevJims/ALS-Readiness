"""add lesson and module table, add a deleted value in structure status, and deleted_at attribute in learning_strands

Revision ID: 2e7189e345fd
Revises: 01e062d32564
Create Date: 2026-09-24 13:40:45.027261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '2e7189e345fd'
down_revision: Union[str, Sequence[str], None] = '01e062d32564'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add the new enum value to the EXISTING structure_status type first
    op.execute("ALTER TYPE structure_status ADD VALUE IF NOT EXISTS 'deleted'")

    # 2. Reference the existing type without trying to (re)create it
    structure_status_enum = postgresql.ENUM(
        'active', 'archived', 'deleted',
        name='structure_status',
        create_type=False,
    )

    op.create_table('modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('strand_id', sa.Integer(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('status', structure_status_enum, nullable=False, server_default='active'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['strand_id'], ['learning_strands.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lessons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('status', structure_status_enum, nullable=False, server_default='active'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('content_evaluations')
    op.drop_table('learning_contents')
    op.alter_column('cohorts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('cohorts', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.drop_constraint(op.f('uq_cohorts_name_school_year'), 'cohorts', type_='unique')
    op.add_column('learning_strands', sa.Column('deleted_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('learning_strands', 'deleted_at')
    op.create_unique_constraint(op.f('uq_cohorts_name_school_year'), 'cohorts', ['name', 'school_year'], postgresql_nulls_not_distinct=False)
    op.alter_column('cohorts', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('cohorts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.create_table('content_evaluations',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('content_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('stimulus_level', postgresql.ENUM('low', 'medium', 'high', name='stimulus_level'), autoincrement=False, nullable=False),
        sa.Column('cognitive_sustainability_rating', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['content_id'], ['learning_contents.id'], name=op.f('content_evaluations_content_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('content_evaluations_pkey'))
    )
    op.create_table('learning_contents',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('strand_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('type', postgresql.ENUM('video', 'audio', 'reading', name='content_type'), autoincrement=False, nullable=False),
        sa.Column('status', postgresql.ENUM('pending', 'active', 'inactive', 'rejected', name='content_status'), autoincrement=False, nullable=False),
        sa.Column('file_path', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('uploaded_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['strand_id'], ['learning_strands.id'], name=op.f('learning_contents_strand_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('learning_contents_pkey'))
    )
    op.drop_table('lessons')
    op.drop_table('modules')