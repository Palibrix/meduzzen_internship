"""Add Action, m2m company models

Revision ID: e5e5c5215bbe
Revises: e7e0c7682c20
Create Date: 2023-10-15 12:51:54.146122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e5e5c5215bbe'
down_revision: Union[str, None] = 'e7e0c7682c20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('actions',
    sa.Column('action_id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('company_id', sa.Integer(), nullable=False),
            sa.Column('action', sa.Enum('request', 'invite', name='action_type'), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('action_id')
    )
    op.create_index(op.f('ix_actions_action_id'), 'actions', ['action_id'], unique=False)
    op.create_table('company_members',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'company_id')
    )


def downgrade() -> None:
    op.drop_table('company_members')
    op.drop_index(op.f('ix_actions_action_id'), table_name='actions')
    op.drop_table('actions')
