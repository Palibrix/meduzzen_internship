"""Add User model

Revision ID: 982968db85d9
Revises: 
Create Date: 2023-09-25 20:55:43.750965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '982968db85d9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(), nullable=False),
    sa.Column('user_firstname', sa.String(), nullable=False),
    sa.Column('user_lastname', sa.String(), nullable=False),
    sa.Column('user_city', sa.String(), nullable=True),
    sa.Column('user_phone', sa.String(), nullable=True),
    sa.Column('user_avatar', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_user_email'), 'users', ['user_email'], unique=True)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_user_email'), table_name='users')
    op.drop_table('users')
