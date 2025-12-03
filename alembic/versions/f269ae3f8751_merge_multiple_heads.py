"""merge multiple heads

Revision ID: f269ae3f8751
Revises: 446a8ffa73d3, 20251011_create_chapter_contents
Create Date: 2025-10-11 15:18:09.907472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f269ae3f8751'
down_revision: Union[str, Sequence[str], None] = ('446a8ffa73d3', '20251011_create_chapter_contents')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
