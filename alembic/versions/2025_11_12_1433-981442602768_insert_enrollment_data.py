"""insert_enrollment_data

Revision ID: 981442602768
Revises: 3a85e743c2ec
Create Date: 2025-11-12 14:33:13.872003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '981442602768'
down_revision = '3a85e743c2ec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert enrollment data (60 records)
    # Grade-Point: A+=4.5, A0=4.0, B+=3.5, B0=3.0, C+=2.5, C0=2.0, F=0.0
    op.execute("""
        INSERT INTO enrollment (student_id, lecture_id, grade)
        VALUES
        -- 이민준 (S1000001): 2025-1 (GPA 4.00), 2025-2 (GPA 3.50)
        ('S1000001', 1, 'A+'), ('S1000001', 2, 'A0'), ('S1000001', 5, 'B+'),
        ('S1000001', 7, 'A0'), ('S1000001', 8, 'B+'), ('S1000001', 11, 'B0'),
        -- 박서아 (S1000002): 2025-1 (GPA 3.00), 2025-2 (GPA 3.17)
        ('S1000002', 1, 'B0'), ('S1000002', 2, 'C+'), ('S1000002', 5, 'B+'),
        ('S1000002', 7, 'B+'), ('S1000002', 8, 'B0'), ('S1000002', 11, 'B0'),
        -- 김주원 (S1000003): 2025-1 (GPA 4.00), 2025-2 (GPA 4.17)
        ('S1000003', 1, 'A0'), ('S1000003', 2, 'A0'), ('S1000003', 3, 'A0'),
        ('S1000003', 7, 'A+'), ('S1000003', 8, 'A0'), ('S1000003', 9, 'A0'),
        -- 최예린 (S1000004): 2025-1 (GPA 3.50), 2025-2 (GPA 3.50)
        ('S1000004', 1, 'B+'), ('S1000004', 2, 'B+'), ('S1000004', 5, 'B+'),
        ('S1000004', 7, 'B+'), ('S1000004', 8, 'B+'), ('S1000004', 11, 'B+'),
        -- 강지후 (S1000005): 2025-1 (GPA 3.63), 2025-2 (GPA 3.69)
        ('S1000005', 3, 'A0'), ('S1000005', 4, 'A0'), ('S1000005', 1, 'B0'),
        ('S1000005', 9, 'A0'), ('S1000005', 10, 'B+'), ('S1000005', 7, 'B+'),
        -- 윤하윤 (S1000006): 2025-1 (GPA 2.44), 2025-2 (GPA 2.94)
        ('S1000006', 3, 'C+'), ('S1000006', 4, 'B0'), ('S1000006', 1, 'C0'),
        ('S1000006', 9, 'B0'), ('S1000006', 10, 'B+'), ('S1000006', 7, 'C+'),
        -- 정시우 (S1000007): 2025-1 (GPA 4.31), 2025-2 (GPA 4.19)
        ('S1000007', 3, 'A+'), ('S1000007', 4, 'A+'), ('S1000007', 5, 'A0'),
        ('S1000007', 9, 'A+'), ('S1000007', 10, 'A0'), ('S1000007', 11, 'A0'),
        -- 백도윤 (S1000008): 2025-1 (GPA 3.21), 2025-2 (GPA 3.50)
        ('S1000008', 5, 'B+'), ('S1000008', 6, 'B0'), ('S1000008', 1, 'B0'),
        ('S1000008', 11, 'B+'), ('S1000008', 12, 'B+'), ('S1000008', 7, 'B+'),
        -- 신채원 (S1000009): 2025-1 (GPA 3.93), 2025-2 (GPA 3.79)
        ('S1000009', 5, 'A0'), ('S1000009', 6, 'B+'), ('S1000009', 3, 'A0'),
        ('S1000009', 11, 'A0'), ('S1000009', 12, 'A0'), ('S1000009', 9, 'B+'),
        -- 한지아 (S1000010): 2025-1 (GPA 2.21), 2025-2 (GPA 2.71)
        ('S1000010', 5, 'C0'), ('S1000010', 6, 'C0'), ('S1000010', 1, 'C+'),
        ('S1000010', 11, 'B0'), ('S1000010', 12, 'C+'), ('S1000010', 7, 'C+')
    """)

    # Insert additional enrollment data for new students
    # Note: lecture_id values need to be determined based on the actual lecture table
    # Using placeholder values - should be updated with actual lecture_ids
    op.execute("""
        INSERT INTO enrollment (student_id, lecture_id, grade)
        VALUES
        -- 박지훈 (S1000011): 2과목 수강
        ('S1000011', (SELECT lecture_id FROM lecture WHERE course_code = 'BUS101' AND semester = '2025-2' AND professor_id = 'P4001'), 'A+'),
        ('S1000011', (SELECT lecture_id FROM lecture WHERE course_code = 'BUS102' AND semester = '2025-2' AND professor_id = 'P4002'), 'A0'),
        -- 이서연 (S1000012): 2과목 수강
        ('S1000012', (SELECT lecture_id FROM lecture WHERE course_code = 'BUS101' AND semester = '2025-2' AND professor_id = 'P4001'), 'B+'),
        ('S1000012', (SELECT lecture_id FROM lecture WHERE course_code = 'BUS201' AND semester = '2025-2' AND professor_id = 'P4001'), 'A0'),
        -- 정예슬 (S1000013): 2과목 수강
        ('S1000013', (SELECT lecture_id FROM lecture WHERE course_code = 'DES101' AND semester = '2025-2' AND professor_id = 'P5001'), 'A0'),
        ('S1000013', (SELECT lecture_id FROM lecture WHERE course_code = 'DES102' AND semester = '2025-2' AND professor_id = 'P5001'), 'A+')
    """)


def downgrade() -> None:
    # Delete enrollment data
    op.execute("DELETE FROM enrollment WHERE student_id LIKE 'S10000%' OR student_id IN ('S2001', 'S2002', 'S3001')")
