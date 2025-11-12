"""create_student_table

Revision ID: c2068e074906
Revises: e853c8733230
Create Date: 2025-11-12 14:03:16.496948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2068e074906'
down_revision = 'e853c8733230'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create student table
    op.create_table(
        'student',
        sa.Column('student_id', sa.CHAR(8), primary_key=True),
        sa.Column('student_name', sa.String(20), nullable=False),
        sa.Column('grade_year', sa.Numeric(1, 0), nullable=False),
        sa.Column('enrollment_status', sa.String(10), nullable=False),
        sa.Column('overall_gpa', sa.Numeric(3, 2), nullable=False),
        sa.Column('dept_code', sa.String(10)),
        sa.ForeignKeyConstraint(['dept_code'], ['department.dept_code']),
        sa.CheckConstraint('grade_year BETWEEN 1 AND 4', name='student_grade_year_check'),
        sa.CheckConstraint("enrollment_status IN ('재학', '휴학', '졸업')", name='student_enrollment_status_check'),
        sa.CheckConstraint('overall_gpa BETWEEN 0.00 AND 4.50', name='student_overall_gpa_check')
    )


def downgrade() -> None:
    # Drop student table
    op.drop_table('student')
