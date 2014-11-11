"""add 180-day columns to address_summaries

Revision ID: 42b7d00d7467
Revises: 3f232866635a
Create Date: 2014-11-10 22:50:34.062595

"""

# revision identifiers, used by Alembic.
revision = '42b7d00d7467'
down_revision = '3f232866635a'

from alembic import op
import sqlalchemy as sa


def upgrade():
	# @todo: Determine how to make these columns get added after the _prev90 ones.
    op.add_column('address_summaries', sa.Column('fire_incidents_last180', sa.Integer))
    op.add_column('address_summaries', sa.Column('fire_incidents_prev180', sa.Integer))
    op.add_column('address_summaries', sa.Column('police_incidents_last180', sa.Integer))
    op.add_column('address_summaries', sa.Column('police_incidents_prev180', sa.Integer))
    pass


def downgrade():
    op.drop_column('address_summaries', 'fire_incidents_last180')
    op.drop_column('address_summaries', 'fire_incidents_prev180')
    op.drop_column('address_summaries', 'police_incidents_last180')
    op.drop_column('address_summaries', 'police_incidents_prev180')
    pass
