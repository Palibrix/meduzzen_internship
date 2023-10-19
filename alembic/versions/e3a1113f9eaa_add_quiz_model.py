"""Add Quiz model

Revision ID: e3a1113f9eaa
Revises: e13e9fb28484
Create Date: 2023-10-19 11:00:15.886850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e3a1113f9eaa'
down_revision: Union[str, None] = 'e13e9fb28484'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('quizzes',
    sa.Column('quiz_id', sa.Integer(), nullable=False),
            sa.Column('quiz_name', sa.String(length=30), nullable=False),
            sa.Column('quiz_title', sa.String(length=30), nullable=False),
            sa.Column('quiz_description', sa.String(length=70), nullable=False),
            sa.Column('quiz_frequency', sa.Integer(), nullable=True),
            sa.Column('quiz_company_id', sa.Integer(), nullable=True),
            sa.Column('created_by', sa.Integer(), nullable=True),
            sa.Column('updated_by', sa.Integer(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(['created_by'], ['users.user_id'], ),
            sa.ForeignKeyConstraint(['quiz_company_id'], ['companies.company_id'], ),
            sa.ForeignKeyConstraint(['updated_by'], ['users.user_id'], ),
            sa.PrimaryKeyConstraint('quiz_id')
    )
    op.create_index(op.f('ix_quizzes_quiz_id'), 'quizzes', ['quiz_id'], unique=False)
    op.create_table('questions',
    sa.Column('question_id', sa.Integer(), nullable=False),
            sa.Column('question_text', sa.String(), nullable=False),
            sa.Column('answer_options', sa.ARRAY(sa.String()), nullable=False),
            sa.Column('correct_answer', sa.Integer(), nullable=False),
            sa.Column('quiz_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.quiz_id'], ),
            sa.PrimaryKeyConstraint('question_id')
    )
    op.create_index(op.f('ix_questions_question_id'), 'questions', ['question_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_questions_question_id'), table_name='questions')
    op.drop_table('questions')
    op.drop_index(op.f('ix_quizzes_quiz_id'), table_name='quizzes')
    op.drop_table('quizzes')
