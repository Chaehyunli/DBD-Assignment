"""insert_lecture_data

Revision ID: 3a85e743c2ec
Revises: 7050ba2057b4
Create Date: 2025-11-12 14:33:06.367638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a85e743c2ec'
down_revision = '7050ba2057b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert lecture data for 2025-1 semester (6 records)
    op.execute("""
        INSERT INTO lecture (semester, lecture_time, lecture_room, capacity, course_code, professor_id)
        VALUES
        ('2025-1', '월 1-2, 수 1', '공학관 110호', 100, 'CS101', 'P0001'),
        ('2025-1', '월 3-4, 수 2', '공학관 111호', 100, 'CS201', 'P0002'),
        ('2025-1', '화 1-2, 목 1', '공학관 210호', 100, 'ME101', 'P0003'),
        ('2025-1', '화 3-4, 목 2', '공학관 211호', 100, 'ME201', 'P0003'),
        ('2025-1', '수 5-6, 금 1', '공학관 310호', 100, 'EE101', 'P0004'),
        ('2025-1', '수 7-8, 금 2', '공학관 311호', 100, 'EE201', 'P0005')
    """)

    # Insert lecture data for 2025-2 semester (6 records)
    op.execute("""
        INSERT INTO lecture (semester, lecture_time, lecture_room, capacity, course_code, professor_id)
        VALUES
        ('2025-2', '월 1-2, 수 1', '공학관 110호', 100, 'CS101', 'P0001'),
        ('2025-2', '월 3-4, 수 2', '공학관 111호', 100, 'CS201', 'P0002'),
        ('2025-2', '화 1-2, 목 1', '공학관 210호', 100, 'ME101', 'P0003'),
        ('2025-2', '화 3-4, 목 2', '공학관 211호', 100, 'ME201', 'P0003'),
        ('2025-2', '수 5-6, 금 1', '공학관 310호', 100, 'EE101', 'P0004'),
        ('2025-2', '수 7-8, 금 2', '공학관 311호', 100, 'EE201', 'P0005')
    """)

    # Insert additional lecture data for 2025-2 semester (5 records)
    op.execute("""
        INSERT INTO lecture (semester, lecture_time, lecture_room, capacity, course_code, professor_id)
        VALUES
        ('2025-2', '월3,4', '경영관 303호', 50, 'BUS101', 'P4001'),
        ('2025-2', '화1,2', '경영관 304호', 50, 'BUS102', 'P4002'),
        ('2025-2', '수5,6', '경영관 303호', 40, 'BUS201', 'P4001'),
        ('2025-2', '화1,2,3', '조형관 105호', 30, 'DES101', 'P5001'),
        ('2025-2', '목1,2', '조형관 202호', 30, 'DES102', 'P5001')
    """)


def downgrade() -> None:
    # Delete lecture data
    op.execute("DELETE FROM lecture WHERE semester IN ('2025-1', '2025-2')")
