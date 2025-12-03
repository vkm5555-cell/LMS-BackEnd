"""create chapter_contents table

Revision ID: 20251011_create_chapter_contents
Revises:
Create Date: 2025-10-11 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251011_create_chapter_contents'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():


    # Create chapter_contents table
    op.create_table(
        'chapter_contents',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('chapter_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer,  nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('slug', sa.String(255), nullable=True),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('content_type', sa.Text, nullable=False),
        sa.Column('content_url', sa.Text, nullable=False),
        sa.Column('video_duration', sa.Integer, nullable=False),
        sa.Column('position', sa.Integer, nullable=False),
        sa.Column('is_published', sa.Boolean, nullable=False, server_default=sa.sql.expression.false()),
        sa.Column('is_free', sa.Boolean, nullable=False, server_default=sa.sql.expression.true()),
        sa.Column('thumbnail_url', sa.Text, nullable=False),
        sa.Column('meta_data', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

def downgrade():
    # Drop table
    op.drop_table('chapter_contents')


