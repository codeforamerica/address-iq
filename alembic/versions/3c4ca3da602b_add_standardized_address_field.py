"""add standardized_address field

Revision ID: 3c4ca3da602b
Revises: 3f232866635a
Create Date: 2014-10-22 10:18:09.641422

"""

# revision identifiers, used by Alembic.
revision = '3c4ca3da602b'
down_revision = '3f232866635a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('fire_incidents', sa.Column('standardized_address', sa.String))
    op.add_column('police_incidents', sa.Column('standardized_address', sa.String))
    op.create_index('ix_fire_standard_address', 'fire_incidents', ['standardized_address'])
    op.create_index('ix_police_standard_address', 'police_incidents', ['standardized_address'])


def downgrade():
    op.drop_column('fire_incidents', 'standardized_address')
    op.drop_column('police_incidents', 'standardized_address')
