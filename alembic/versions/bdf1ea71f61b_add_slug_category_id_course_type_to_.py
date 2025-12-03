"""add slug, category_id, course_type to courses

Revision ID: bdf1ea71f61b
Revises: edd85781229b
Create Date: 2025-09-19 10:08:03.175105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'bdf1ea71f61b'
down_revision: Union[str, Sequence[str], None] = 'edd85781229b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("courses", sa.Column("course_mode", sa.String(length=50), nullable=False, server_default="online"))
    op.add_column("courses", sa.Column("course_price", sa.Float(), nullable=False, server_default="0"))

def downgrade() -> None:
    op.drop_column("courses", "course_price")
    op.drop_column("courses", "course_mode")