"""create discussions and discussion_comments tables"""

from alembic import op
import sqlalchemy as sa

revision = '20250101_create_discussion_tables'
down_revision = 'c39e11512bca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'discussions',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),

        sa.Column('course_id', sa.BigInteger, nullable=False),
        sa.Column('chapter_id', sa.BigInteger, nullable=False),
        sa.Column('content_id', sa.BigInteger, nullable=False),

        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),

        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('likes', sa.Integer, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP,
                  server_default=sa.text('CURRENT_TIMESTAMP'),
                  onupdate=sa.text('CURRENT_TIMESTAMP'))
    )

    op.create_table(
        'discussion_comments',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),

        sa.Column('course_id', sa.BigInteger, nullable=False),
        sa.Column('chapter_id', sa.BigInteger, nullable=False),
        sa.Column('content_id', sa.BigInteger, nullable=False),

        sa.Column('discussion_id', sa.BigInteger,
                  sa.ForeignKey('discussions.id', ondelete="CASCADE"),
                  nullable=False),

        sa.Column('user_id', sa.Integer,
                  sa.ForeignKey('users.id'),
                  nullable=False),

        sa.Column('parent_id', sa.BigInteger,
                  sa.ForeignKey('discussion_comments.id', ondelete="CASCADE"),
                  nullable=True),

        sa.Column('content', sa.Text, nullable=False),
        sa.Column('likes', sa.Integer, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP'))
    )


def downgrade():
    op.drop_table('discussion_comments')
    op.drop_table('discussions')
