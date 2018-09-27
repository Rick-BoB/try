"""empty message

Revision ID: 2b68ca632804
Revises: 034d6ee74a60
Create Date: 2018-09-27 10:44:03.080846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b68ca632804'
down_revision = '034d6ee74a60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('referral', sa.Column('paid', sa.Boolean(), nullable=True))
    op.add_column('referral', sa.Column('referred_by_id', sa.Integer(), nullable=False))
    op.add_column('referral', sa.Column('referred_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_referral_referred_by_id'), 'referral', ['referred_by_id'], unique=False)
    op.create_index(op.f('ix_referral_referred_id'), 'referral', ['referred_id'], unique=False)
    op.drop_index('ix_referral_cellphone', table_name='referral')
    op.drop_index('ix_referral_seller_id', table_name='referral')
    op.drop_constraint('referral_seller_id_fkey', 'referral', type_='foreignkey')
    op.create_foreign_key(None, 'referral', 'seller', ['referred_id'], ['id'], initially='DEFERRED', deferrable=True)
    op.create_foreign_key(None, 'referral', 'seller', ['referred_by_id'], ['id'], initially='DEFERRED', deferrable=True)
    op.drop_column('referral', 'first_name')
    op.drop_column('referral', 'description')
    op.drop_column('referral', 'seller_id')
    op.drop_column('referral', 'cellphone')
    op.drop_column('referral', 'last_name')
    op.add_column('seller', sa.Column('referred_by_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_seller_referred_by_id'), 'seller', ['referred_by_id'], unique=False)
    op.drop_index('ix_seller_referred_by', table_name='seller')
    op.drop_constraint('seller_referred_by_fkey', 'seller', type_='foreignkey')
    op.create_foreign_key(None, 'seller', 'seller', ['referred_by_id'], ['id'], initially='DEFERRED', deferrable=True)
    op.drop_column('seller', 'referred_by')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seller', sa.Column('referred_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'seller', type_='foreignkey')
    op.create_foreign_key('seller_referred_by_fkey', 'seller', 'seller', ['referred_by'], ['id'], initially='DEFERRED', deferrable=True)
    op.create_index('ix_seller_referred_by', 'seller', ['referred_by'], unique=False)
    op.drop_index(op.f('ix_seller_referred_by_id'), table_name='seller')
    op.drop_column('seller', 'referred_by_id')
    op.add_column('referral', sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('referral', sa.Column('cellphone', sa.BIGINT(), autoincrement=False, nullable=False))
    op.add_column('referral', sa.Column('seller_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('referral', sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('referral', sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'referral', type_='foreignkey')
    op.drop_constraint(None, 'referral', type_='foreignkey')
    op.create_foreign_key('referral_seller_id_fkey', 'referral', 'seller', ['seller_id'], ['id'], initially='DEFERRED', deferrable=True)
    op.create_index('ix_referral_seller_id', 'referral', ['seller_id'], unique=False)
    op.create_index('ix_referral_cellphone', 'referral', ['cellphone'], unique=True)
    op.drop_index(op.f('ix_referral_referred_id'), table_name='referral')
    op.drop_index(op.f('ix_referral_referred_by_id'), table_name='referral')
    op.drop_column('referral', 'referred_id')
    op.drop_column('referral', 'referred_by_id')
    op.drop_column('referral', 'paid')
    # ### end Alembic commands ###
