"""Add on delete constraints

Revision ID: e7e0c7682c20
Revises: 8c3c776e7f28
Create Date: 2023-10-13 17:38:12.761593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e7e0c7682c20'
down_revision: Union[str, None] = '8c3c776e7f28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('companies_company_owner_id_fkey', 'companies', type_='foreignkey')
    op.create_foreign_key(None, 'companies', 'users', ['company_owner_id'], ['user_id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'companies', type_='foreignkey')
    op.create_foreign_key('companies_company_owner_id_fkey', 'companies', 'users', ['company_owner_id'], ['user_id'])
