"""add show leaderboard setting

Revision ID: a1b2c3d4e5f6
Revises: 9b1f2c3d4e5f
Create Date: 2026-05-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f6'
down_revision = '9b1f2c3d4e5f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('show_leaderboard', sa.Boolean(), nullable=False, server_default=sa.true()))


def downgrade():
    with op.batch_alter_table('settings', schema=None) as batch_op:
        batch_op.drop_column('show_leaderboard')
