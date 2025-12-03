"""merge heads

Revision ID: b92d489f78fc
Revises: c39e11512bca, 20250101_create_discussion_tables
Create Date: 2025-12-01 10:58:00.257087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b92d489f78fc'
down_revision: Union[str, Sequence[str], None] = ('c39e11512bca', '20250101_create_discussion_tables')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
