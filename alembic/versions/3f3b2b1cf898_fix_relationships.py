"""fix relationships

Revision ID: 3f3b2b1cf898
Revises: f269ae3f8751
Create Date: 2025-10-14 12:16:51.075773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3f3b2b1cf898'
down_revision: Union[str, Sequence[str], None] = 'f269ae3f8751'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
    # op.create_table('course_instructors',
    # sa.Column('course_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    # sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    # sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name=op.f('course_instructors_ibfk_1'), ondelete='CASCADE'),
    # sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('course_instructors_ibfk_2'), ondelete='CASCADE'),
    # sa.PrimaryKeyConstraint('course_id', 'user_id'),
    # mysql_collate='utf8mb4_general_ci',
    # mysql_default_charset='utf8mb4',
    # mysql_engine='InnoDB'
    # )
    # ### end Alembic commands ###
