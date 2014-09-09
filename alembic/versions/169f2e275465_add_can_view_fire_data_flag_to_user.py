"""add can_view_fire_data flag to user

Revision ID: 169f2e275465
Revises: 1ee76cf990d9
Create Date: 2014-09-05 01:55:56.983731

"""

# revision identifiers, used by Alembic.
revision = '169f2e275465'
down_revision = '43c6e3f2548a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('can_view_fire_data', sa.Boolean))


def downgrade():
    op.drop_column('users', 'can_view_fire_data')
