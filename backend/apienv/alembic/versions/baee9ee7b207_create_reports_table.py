"""create reports table

Revision ID: baee9ee7b207
Revises: 
Create Date: 2023-04-07 11:07:08.969718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'baee9ee7b207'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'reports',
        sa.Column('post_id', sa.Integer, sa.ForeignKey(
            "posts.id"), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey(
            "users.id"), primary_key=True),
        sa.Column('reason', sa.VARCHAR(250), nullable=False),
    )


def downgrade():
    op.drop_table('reports')
