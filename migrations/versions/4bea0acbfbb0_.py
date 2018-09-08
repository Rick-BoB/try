"""empty message

Revision ID: 4bea0acbfbb0
Revises: 0ff32742b39f
Create Date: 2018-09-08 07:40:35.205353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4bea0acbfbb0'
down_revision = '0ff32742b39f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seller', sa.Column('time_duing_DS', sa.Interval(), nullable=True))
    op.drop_column('seller', 'income_from_DS')
    op.drop_column('seller', 'time_investment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seller', sa.Column('time_investment', postgresql.INTERVAL(), autoincrement=False, nullable=True))
    op.add_column('seller', sa.Column('income_from_DS', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True))
    op.drop_column('seller', 'time_duing_DS')
    # ### end Alembic commands ###
