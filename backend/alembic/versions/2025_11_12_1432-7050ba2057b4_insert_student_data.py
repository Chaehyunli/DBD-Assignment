"""insert_student_data

Revision ID: 7050ba2057b4
Revises: 93a601100ba9
Create Date: 2025-11-12 14:32:59.138422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7050ba2057b4'
down_revision = '93a601100ba9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert student data (10 records)
    op.execute("""
        INSERT INTO student (student_id, student_name, grade_year, enrollment_status, overall_gpa, dept_code)
        VALUES
        ('S1000001', '이민준', 1, '재학', 3.75, 'CS'),
        ('S1000002', '박서아', 1, '재학', 3.08, 'CS'),
        ('S1000003', '김주원', 2, '재학', 4.08, 'CS'),
        ('S1000004', '최예린', 2, '재학', 3.50, 'CS'),
        ('S1000005', '강지후', 1, '재학', 3.66, 'ME'),
        ('S1000006', '윤하윤', 2, '재학', 2.69, 'ME'),
        ('S1000007', '정시우', 3, '재학', 4.25, 'ME'),
        ('S1000008', '백도윤', 1, '재학', 3.36, 'EE'),
        ('S1000009', '신채원', 2, '재학', 3.86, 'EE'),
        ('S1000010', '한지아', 3, '재학', 2.46, 'EE')
    """)


def downgrade() -> None:
    # Delete student data
    op.execute("DELETE FROM student WHERE student_id LIKE 'S10000%'")
