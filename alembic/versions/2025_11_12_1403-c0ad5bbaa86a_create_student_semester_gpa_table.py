"""create_student_semester_gpa_table

Revision ID: c0ad5bbaa86a
Revises: b3b0e82d4f72
Create Date: 2025-11-12 14:03:39.253395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0ad5bbaa86a'
down_revision = 'b3b0e82d4f72'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create student_semester_gpa table
    op.create_table(
        'student_semester_gpa',
        sa.Column('student_id', sa.CHAR(8), nullable=False),
        sa.Column('semester', sa.String(6), nullable=False),
        sa.Column('semester_gpa', sa.Numeric(3, 2), nullable=False),
        sa.Column('earned_credits', sa.Numeric(3, 0), nullable=False),
        sa.PrimaryKeyConstraint('student_id', 'semester'),
        sa.ForeignKeyConstraint(['student_id'], ['student.student_id'], ondelete='CASCADE'),
        sa.CheckConstraint('semester_gpa BETWEEN 0.00 AND 4.50', name='student_semester_gpa_check'),
        sa.CheckConstraint('earned_credits >= 0', name='student_earned_credits_check')
    )


def downgrade() -> None:
    # Drop student_semester_gpa table
    op.drop_table('student_semester_gpa')
