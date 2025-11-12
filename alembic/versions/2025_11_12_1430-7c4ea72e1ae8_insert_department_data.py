"""insert_department_data

Revision ID: 7c4ea72e1ae8
Revises: c0ad5bbaa86a
Create Date: 2025-11-12 14:30:23.637005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c4ea72e1ae8'
down_revision = 'c0ad5bbaa86a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert department data (3 records)
    op.execute("""
        INSERT INTO department (dept_code, dept_name, office_location, office_phone_number)
        VALUES
        ('CS', '컴퓨터공학과', '공학관 101호', '02-111-1111'),
        ('ME', '기계공학과', '공학관 201호', '02-222-2222'),
        ('EE', '전자공학과', '공학관 301호', '02-333-3333')
    """)


def downgrade() -> None:
    # Delete department data
    op.execute("DELETE FROM department WHERE dept_code IN ('CS', 'ME', 'EE')")
