"""add quantity column to cart

Revision ID: 264b12906998
Revises: e7dd6209efcf
Create Date: 2025-03-18 19:12:32.025760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '264b12906998'
down_revision = 'e7dd6209efcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False,server_default='1'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###
