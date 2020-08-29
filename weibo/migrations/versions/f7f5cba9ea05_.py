"""empty message

Revision ID: f7f5cba9ea05
Revises: 3efa542ddd6b
Create Date: 2020-08-27 08:13:19.010870

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f7f5cba9ea05'
down_revision = '3efa542ddd6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weibo', sa.Column('uid', sa.Integer(), nullable=False))
    op.drop_index('ix_weibo_title', table_name='weibo')
    op.drop_column('weibo', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weibo', sa.Column('title', mysql.VARCHAR(length=50), nullable=False))
    op.create_index('ix_weibo_title', 'weibo', ['title'], unique=False)
    op.drop_column('weibo', 'uid')
    # ### end Alembic commands ###