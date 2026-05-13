"""add user nickname

Revision ID: 9b1f2c3d4e5f
Revises: 16e9bbd382da
Create Date: 2026-05-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '9b1f2c3d4e5f'
down_revision = '16e9bbd382da'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nickname', sa.String(length=64), nullable=True))

    op.execute("UPDATE user SET nickname = substr(email, 1, instr(email, '@') - 1) WHERE nickname IS NULL")

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('nickname', existing_type=sa.String(length=64), nullable=False)


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('nickname')
