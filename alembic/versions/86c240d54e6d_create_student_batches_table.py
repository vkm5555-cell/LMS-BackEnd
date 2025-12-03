from alembic import op
import sqlalchemy as sa

revision = '86c240d54e6d'
down_revision = '3f3b2b1cf898'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'student_batches',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('semester_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive'), server_default='active'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),

        # ✅ Correct Foreign Keys
        # sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        # sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ondelete='CASCADE'),
        # sa.ForeignKeyConstraint(['course_id'], ['course.id'], ondelete='CASCADE'),
        # sa.ForeignKeyConstraint(['session_id'], ['session.id'], ondelete='CASCADE'),
        # sa.ForeignKeyConstraint(['semester_id'], ['semester.id'], ondelete='CASCADE'),
    )

def downgrade():
    op.drop_table('student_batches')
