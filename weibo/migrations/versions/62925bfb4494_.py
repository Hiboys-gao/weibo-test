"""empty message

Revision ID: 62925bfb4494
Revises: c94358b871a8
Create Date: 2020-08-27 08:15:14.201459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62925bfb4494'
down_revision = 'c94358b871a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weibo', sa.Column('uid', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_weibo_uid'), 'weibo', ['uid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_weibo_uid'), table_name='weibo')
    op.drop_column('weibo', 'uid')
    # ### end Alembic commands ###
