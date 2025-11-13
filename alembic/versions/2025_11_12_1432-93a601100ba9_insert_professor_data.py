"""insert_professor_data

Revision ID: 93a601100ba9
Revises: ed8b920fd1d1
Create Date: 2025-11-12 14:32:05.377526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93a601100ba9'
down_revision = 'ed8b920fd1d1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert professor data (5 records)
    op.execute("""
        INSERT INTO professor (professor_id, professor_name, office_room, email, dept_code)
        VALUES
        ('P0001', '김철수', '공학관 102호', 'kim@univ.ac.kr', 'CS'),
        ('P0002', '이영희', '공학관 103호', 'lee@univ.ac.kr', 'CS'),
        ('P0003', '박현우', '공학관 202호', 'park@univ.ac.kr', 'ME'),
        ('P0004', '최지민', '공학관 302호', 'choi@univ.ac.kr', 'EE'),
        ('P0005', '정다빈', '공학관 303호', 'jung@univ.ac.kr', 'EE')
    """)

    # Insert additional professor data (3 records)
    op.execute("""
        INSERT INTO professor (professor_id, professor_name, office_room, email, dept_code)
        VALUES
        ('P4001', '김영민', '경영관 501호', 'ymkim@mju.ac.kr', 'BUS'),
        ('P4002', '이하나', '경영관 502호', 'hnlee@mju.ac.kr', 'BUS'),
        ('P5001', '최미소', '조형관 302호', 'mschoi@mju.ac.kr', 'DES')
    """)


def downgrade() -> None:
    # Delete professor data
    op.execute("DELETE FROM professor WHERE professor_id IN ('P0001', 'P0002', 'P0003', 'P0004', 'P0005', 'P4001', 'P4002', 'P5001')")
