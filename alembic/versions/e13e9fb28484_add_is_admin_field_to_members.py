"""Add is_admin field to members

Revision ID: e13e9fb28484
Revises: e5e5c5215bbe
Create Date: 2023-10-17 18:18:29.741228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e13e9fb28484'
down_revision: Union[str, None] = 'e5e5c5215bbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('company_members', sa.Column('is_admin', sa.Boolean()))


def downgrade() -> None:
    op.drop_column('company_members', 'is_admin')
