"""empty message

Revision ID: fd584542ea33
Revises: 34e025f202c1
Create Date: 2018-09-03 14:18:36.094369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd584542ea33'
down_revision = '34e025f202c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('date', sa.DateTime(timezone=True), nullable=False))
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.drop_column('order', 'date')
    # ### end Alembic commands ###