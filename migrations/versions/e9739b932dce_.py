"""empty message

Revision ID: e9739b932dce
Revises: 781461d4d943
Create Date: 2018-09-04 07:26:05.464873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9739b932dce'
down_revision = '781461d4d943'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seller', sa.Column('commission', sa.Numeric(precision=2, scale=2), nullable=True))
    op.drop_column('seller', 'comission')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seller', sa.Column('comission', sa.NUMERIC(precision=2, scale=2), autoincrement=False, nullable=True))
    op.drop_column('seller', 'commission')
    # ### end Alembic commands ###
