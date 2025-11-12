"""create_enrollment_table

Revision ID: b3b0e82d4f72
Revises: c391a93ca183
Create Date: 2025-11-12 14:03:35.966959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3b0e82d4f72'
down_revision = 'c391a93ca183'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enrollment table
    op.create_table(
        'enrollment',
        sa.Column('student_id', sa.CHAR(8), nullable=False),
        sa.Column('lecture_id', sa.Integer, nullable=False),
        sa.Column('grade', sa.String(2)),
        sa.PrimaryKeyConstraint('student_id', 'lecture_id'),
        sa.ForeignKeyConstraint(['student_id'], ['student.student_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['lecture_id'], ['lecture.lecture_id'], ondelete='CASCADE')
    )


def downgrade() -> None:
    # Drop enrollment table
    op.drop_table('enrollment')
