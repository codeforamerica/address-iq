"""add address_summaries table

Revision ID: 5932c01014d4
Revises: 4ca6c04c18de
Create Date: 2014-08-06 09:00:49.236200

"""

# revision identifiers, used by Alembic.
revision = '5932c01014d4'
down_revision = '4ca6c04c18de'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'address_summaries',
        sa.Column('address', sa.String(50), primary_key=True),
        sa.Column('business_counts', sa.Integer),
        sa.Column('business_names', sa.Text),
        sa.Column('business_types', sa.Text),
        sa.Column('fire_last7', sa.Integer),
        sa.Column('fire_prior7', sa.Integer),
        sa.Column('police_last7', sa.Integer),
        sa.Column('police_prior7', sa.Integer),
        sa.Column('fire_last30', sa.Integer),
        sa.Column('fire_prior30', sa.Integer),
        sa.Column('police_last30', sa.Integer),
        sa.Column('police_prior30', sa.Integer),
        sa.Column('fire_last90', sa.Integer),
        sa.Column('fire_prior90', sa.Integer),
        sa.Column('police_last90', sa.Integer),
        sa.Column('police_prior90', sa.Integer),
        sa.Column('fire_last365', sa.Integer),
        sa.Column('fire_prior365', sa.Integer),
        sa.Column('police_last365', sa.Integer),
        sa.Column('police_prior365', sa.Integer)
        )


def downgrade():
    op.drop_table('address_summaries')
