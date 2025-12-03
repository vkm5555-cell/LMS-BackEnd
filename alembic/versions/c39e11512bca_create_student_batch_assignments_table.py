"""create student_batch_assignments table

Revision ID: c39e11512bca
Revises: 86c240d54e6d
Create Date: 2025-10-30 10:03:41.619560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c39e11512bca'
down_revision: Union[str, Sequence[str], None] = '86c240d54e6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "student_batch_assignments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("batch_id", sa.Integer(), sa.ForeignKey("student_batches.id", ondelete="CASCADE"), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("student_id", "batch_id", name="uq_student_batch"),
    )

def downgrade() -> None:
    op.drop_table("student_batch_assignments")