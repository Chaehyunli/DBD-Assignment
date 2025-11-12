"""create_course_table

Revision ID: e853c8733230
Revises: fbdb57480d04
Create Date: 2025-11-12 14:02:40.498084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e853c8733230'
down_revision = 'fbdb57480d04'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create course table
    op.create_table(
        'course',
        sa.Column('course_code', sa.String(10), primary_key=True),
        sa.Column('course_name', sa.String(50), nullable=False, unique=True),
        sa.Column('credits', sa.Numeric(1, 0), nullable=False),
        sa.CheckConstraint('credits BETWEEN 1 AND 4', name='course_credits_check')
    )


def downgrade() -> None:
    # Drop course table
    op.drop_table('course')
