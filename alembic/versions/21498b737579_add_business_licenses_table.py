"""Add business licenses table

Revision ID: 21498b737579
Revises: 163459dcf8ed
Create Date: 2014-07-15 09:34:59.399648

"""

# revision identifiers, used by Alembic.
revision = '21498b737579'
down_revision = '163459dcf8ed'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'business_licenses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200)),
        sa.Column('business_class', sa.String(40)),
        sa.Column('business_service_description', sa.String(100)),
        sa.Column('business_product', sa.String(40)),
        sa.Column('business_address', sa.String(200)),
        sa.Column('business_zip', sa.String(20))
    )


def downgrade():
    op.drop_table('business_licenses')
