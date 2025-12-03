"""add user_id to courses

Revision ID: edd85781229b
Revises: 1b92f4f79e17
Create Date: 2025-09-18 11:36:18.810867

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edd85781229b'
down_revision: Union[str, Sequence[str], None] = '1b92f4f79e17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('courses', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_courses_user',   # constraint name
        'courses',           # source table
        'users',             # referent table
        ['user_id'],         # source column
        ['id'],              # referent column
        ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('fk_courses_user', 'courses', type_='foreignkey')
    op.drop_column('courses', 'user_id')