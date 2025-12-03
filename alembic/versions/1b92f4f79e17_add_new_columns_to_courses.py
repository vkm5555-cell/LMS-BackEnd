"""add new columns to courses

Revision ID: 1b92f4f79e17
Revises: fb7a6e96e4c8
Create Date: 2025-09-18 11:23:48.558396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = '1b92f4f79e17'
down_revision: Union[str, Sequence[str], None] = 'fb7a6e96e4c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('courses', sa.Column('subtitle', sa.String(length=255), nullable=True))
    op.add_column('courses', sa.Column('learning_objectives', sa.Text(), nullable=True))
    op.add_column('courses', sa.Column('requirements', sa.Text(), nullable=True))
    op.add_column('courses', sa.Column('language', sa.String(length=50), nullable=False, server_default='English'))
    op.add_column('courses', sa.Column('level', sa.String(length=50), nullable=False, server_default='Beginner'))
    op.add_column('courses', sa.Column('topic_tags', mysql.JSON(), nullable=True))
    op.add_column('courses', sa.Column('image_url', sa.String(length=255), nullable=True))
    op.add_column('courses', sa.Column('promo_video_url', sa.String(length=255), nullable=True))
    op.add_column('courses', sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False))
    op.add_column('courses', sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))


def downgrade():
    op.drop_column('courses', 'updated_at')
    op.drop_column('courses', 'created_at')
    op.drop_column('courses', 'promo_video_url')
    op.drop_column('courses', 'image_url')
    op.drop_column('courses', 'topic_tags')
    op.drop_column('courses', 'level')
    op.drop_column('courses', 'language')
    op.drop_column('courses', 'requirements')
    op.drop_column('courses', 'learning_objectives')
    op.drop_column('courses', 'subtitle')
