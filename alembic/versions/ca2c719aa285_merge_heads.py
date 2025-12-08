"""merge heads

Revision ID: ca2c719aa285
Revises: b92d489f78fc, 20251208_course_assignments
Create Date: 2025-12-08 10:48:10.016344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca2c719aa285'
down_revision: Union[str, Sequence[str], None] = ('b92d489f78fc', '20251208_course_assignments')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
