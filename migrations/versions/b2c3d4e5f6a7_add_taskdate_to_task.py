"""add taskdate to task

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import date


revision = 'b2c3d4e5f6a7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    today = date.today().isoformat()

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('taskdate', sa.String(length=10), nullable=True))

    op.execute(f"UPDATE task SET taskdate = '{today}' WHERE taskdate IS NULL")

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('taskdate', existing_type=sa.String(length=10), nullable=False)


def downgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('taskdate')
