"""add more columns to courses

Revision ID: fb7a6e96e4c8
Revises: 57dbc557d596
Create Date: 2025-09-18 10:52:42.274187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = 'fb7a6e96e4c8'
down_revision: Union[str, Sequence[str], None] = '57dbc557d596'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('courses', sa.Column('subtitle', sa.String(length=255), nullable=True))
    op.add_column('courses', sa.Column('learning_objectives', sa.Text(), nullable=True))
    op.add_column('courses', sa.Column('requirements', sa.Text(), nullable=True))
    op.add_column('courses', sa.Column('language', sa.String(length=50), nullable=False, server_default='English'))
    op.add_column('courses', sa.Column('level', sa.String(length=50), nullable=False, server_default='Beginner'))
    op.add_column('courses', sa.Column('topic_tags', sa.JSON(), nullable=True))
    op.add_column('courses', sa.Column('image_url', sa.String(length=255), nullable=True))
    op.add_column('courses', sa.Column('promo_video_url', sa.String(length=255), nullable=True))
    op.add_column('courses', sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))

def downgrade():
    pass
