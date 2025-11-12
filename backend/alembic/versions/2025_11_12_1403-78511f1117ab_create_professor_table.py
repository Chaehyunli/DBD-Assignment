"""create_professor_table

Revision ID: 78511f1117ab
Revises: c2068e074906
Create Date: 2025-11-12 14:03:29.152818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78511f1117ab'
down_revision = 'c2068e074906'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create professor table
    op.create_table(
        'professor',
        sa.Column('professor_id', sa.CHAR(5), primary_key=True),
        sa.Column('professor_name', sa.String(20), nullable=False),
        sa.Column('office_room', sa.String(50)),
        sa.Column('email', sa.String(50), unique=True),
        sa.Column('dept_code', sa.String(10)),
        sa.ForeignKeyConstraint(['dept_code'], ['department.dept_code'])
    )


def downgrade() -> None:
    # Drop professor table
    op.drop_table('professor')
