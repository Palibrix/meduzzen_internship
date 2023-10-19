"""Add Company model

Revision ID: 8c3c776e7f28
Revises: 982968db85d9
Create Date: 2023-10-13 15:00:13.513396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '8c3c776e7f28'
down_revision: Union[str, None] = '982968db85d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('companies',
    sa.Column('company_id', sa.Integer(), nullable=False),
            sa.Column('company_owner_id', sa.Integer(), nullable=False),
            sa.Column('company_name', sa.String(length=30), nullable=False),
            sa.Column('company_title', sa.String(length=70), nullable=False),
            sa.Column('company_description', sa.String(), nullable=False),
            sa.Column('company_city', sa.String(), nullable=True),
            sa.Column('company_phone', sa.String(), nullable=True),
            sa.Column('company_links', sa.String(), nullable=True),
            sa.Column('company_avatar', sa.String(), nullable=True),
            sa.Column('is_visible', sa.Boolean(), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(['company_owner_id'], ['users.user_id'], ),
            sa.PrimaryKeyConstraint('company_id'),
            sa.UniqueConstraint('company_name')
    )
    op.create_index(op.f('ix_companies_company_id'), 'companies', ['company_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_companies_company_id'), table_name='companies')
    op.drop_table('companies')
