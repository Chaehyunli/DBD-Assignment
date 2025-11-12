"""create_lecture_table

Revision ID: c391a93ca183
Revises: 78511f1117ab
Create Date: 2025-11-12 14:03:32.593460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c391a93ca183'
down_revision = '78511f1117ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create sequence for lecture_id
    op.execute("CREATE SEQUENCE lecture_lecture_id_seq")

    # Create lecture table
    op.create_table(
        'lecture',
        sa.Column('lecture_id', sa.Integer, primary_key=True, nullable=False,
                  server_default=sa.text("nextval('lecture_lecture_id_seq')")),
        sa.Column('semester', sa.String(6), nullable=False),
        sa.Column('lecture_time', sa.String(50)),
        sa.Column('lecture_room', sa.String(50)),
        sa.Column('capacity', sa.Numeric(3, 0), nullable=False),
        sa.Column('course_code', sa.String(10), nullable=False),
        sa.Column('professor_id', sa.CHAR(5)),
        sa.ForeignKeyConstraint(['course_code'], ['course.course_code']),
        sa.ForeignKeyConstraint(['professor_id'], ['professor.professor_id']),
        sa.CheckConstraint('capacity BETWEEN 1 AND 999', name='lecture_capacity_check')
    )

    # Set sequence ownership to the column
    op.execute("ALTER SEQUENCE lecture_lecture_id_seq OWNED BY lecture.lecture_id")


def downgrade() -> None:
    # Drop lecture table (sequence will be dropped automatically due to OWNED BY)
    op.drop_table('lecture')
