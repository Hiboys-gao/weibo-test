"""empty message

Revision ID: fa7c0dab146b
Revises: 3cff985b485d
Create Date: 2020-08-25 20:32:11.408872

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fa7c0dab146b'
down_revision = '3cff985b485d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', mysql.VARCHAR(length=20), nullable=False))
    # ### end Alembic commands ###
