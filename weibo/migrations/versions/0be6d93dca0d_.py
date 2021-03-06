"""empty message

Revision ID: 0be6d93dca0d
Revises: cb73e71b86e0
Create Date: 2020-08-29 09:49:28.606391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0be6d93dca0d'
down_revision = 'cb73e71b86e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow',
    sa.Column('me_uid', sa.Integer(), nullable=False),
    sa.Column('other_uid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('me_uid', 'other_uid')
    )
    op.create_table('thumb',
    sa.Column('me_uid', sa.Integer(), nullable=False),
    sa.Column('other_uid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('me_uid', 'other_uid')
    )
    op.add_column('user', sa.Column('n_fans', sa.Integer(), nullable=False))
    op.add_column('user', sa.Column('n_follow', sa.Integer(), nullable=False))
    op.add_column('weibo', sa.Column('n_thumb', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('weibo', 'n_thumb')
    op.drop_column('user', 'n_follow')
    op.drop_column('user', 'n_fans')
    op.drop_table('thumb')
    op.drop_table('follow')
    # ### end Alembic commands ###
