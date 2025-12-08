"""
Revision ID: 20251208_course_assignments
Revises: f85cf9072aee
Create Date: 2025-12-08
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251208_course_assignments'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'course_assignments',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),

        sa.Column('course_id', sa.Integer, nullable=False, index=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),

        sa.Column('file_path', sa.String(500), nullable=True),
        sa.Column('max_marks', sa.Integer, nullable=False, server_default="100"),
        sa.Column('due_date', sa.DateTime, nullable=True),

        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime,
                  server_default=sa.func.now(),
                  onupdate=sa.func.now()),

        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )


def downgrade():
    op.drop_table('course_assignments')
