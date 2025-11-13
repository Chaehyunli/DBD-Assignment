"""insert_course_data

Revision ID: ed8b920fd1d1
Revises: 7c4ea72e1ae8
Create Date: 2025-11-12 14:31:14.363960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed8b920fd1d1'
down_revision = '7c4ea72e1ae8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert course data (6 records)
    op.execute("""
        INSERT INTO course (course_code, course_name, credits)
        VALUES
        ('CS101', '프로그래밍기초', 3),
        ('CS201', '자료구조', 3),
        ('ME101', '기초역학', 3),
        ('ME201', '열역학', 2),
        ('EE101', '회로이론', 3),
        ('EE201', '전자기학', 1)
    """)

    # Insert additional course data (5 records)
    op.execute("""
        INSERT INTO course (course_code, course_name, credits)
        VALUES
        ('BUS101', '경영학원론', 3),
        ('BUS102', '마케팅', 3),
        ('BUS201', '회계원리', 3),
        ('DES101', '기초디자인', 3),
        ('DES102', '색채학', 2)
    """)


def downgrade() -> None:
    # Delete course data
    op.execute("DELETE FROM course WHERE course_code IN ('CS101', 'CS201', 'ME101', 'ME201', 'EE101', 'EE201', 'BUS101', 'BUS102', 'BUS201', 'DES101', 'DES102')")
