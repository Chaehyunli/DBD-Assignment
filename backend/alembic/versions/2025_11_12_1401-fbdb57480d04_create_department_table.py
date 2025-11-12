"""create_department_table

Revision ID: fbdb57480d04
Revises: 
Create Date: 2025-11-12 14:01:55.840565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbdb57480d04'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create department table
    op.create_table(
        'department',
        sa.Column('dept_code', sa.String(10), primary_key=True),
        sa.Column('dept_name', sa.String(50), nullable=False),
        sa.Column('office_location', sa.String(100)),
        sa.Column('office_phone_number', sa.String(15))
    )


def downgrade() -> None:
    # Drop department table
    op.drop_table('department')
