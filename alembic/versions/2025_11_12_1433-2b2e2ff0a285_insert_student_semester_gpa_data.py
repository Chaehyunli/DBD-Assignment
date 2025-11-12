"""insert_student_semester_gpa_data

Revision ID: 2b2e2ff0a285
Revises: 981442602768
Create Date: 2025-11-12 14:33:21.547095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b2e2ff0a285'
down_revision = '981442602768'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert student_semester_gpa data (20 records)
    op.execute("""
        INSERT INTO student_semester_gpa (student_id, semester, semester_gpa, earned_credits)
        VALUES
        ('S1000001', '2025-1', 4.00, 9),
        ('S1000001', '2025-2', 3.50, 9),
        ('S1000002', '2025-1', 3.00, 9),
        ('S1000002', '2025-2', 3.17, 9),
        ('S1000003', '2025-1', 4.00, 9),
        ('S1000003', '2025-2', 4.17, 9),
        ('S1000004', '2025-1', 3.50, 9),
        ('S1000004', '2025-2', 3.50, 9),
        ('S1000005', '2025-1', 3.63, 8),
        ('S1000005', '2025-2', 3.69, 8),
        ('S1000006', '2025-1', 2.44, 8),
        ('S1000006', '2025-2', 2.94, 8),
        ('S1000007', '2025-1', 4.31, 8),
        ('S1000007', '2025-2', 4.19, 8),
        ('S1000008', '2025-1', 3.21, 7),
        ('S1000008', '2025-2', 3.50, 7),
        ('S1000009', '2025-1', 3.93, 7),
        ('S1000009', '2025-2', 3.79, 7),
        ('S1000010', '2025-1', 2.21, 7),
        ('S1000010', '2025-2', 2.71, 7)
    """)


def downgrade() -> None:
    # Delete student_semester_gpa data
    op.execute("DELETE FROM student_semester_gpa WHERE student_id LIKE 'S10000%'")
