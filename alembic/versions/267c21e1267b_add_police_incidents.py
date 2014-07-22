"""add police incidents

Revision ID: 267c21e1267b
Revises: 1581ef0e0d30
Create Date: 2014-07-22 16:12:34.874600

"""

# revision identifiers, used by Alembic.
revision = '267c21e1267b'
down_revision = '1581ef0e0d30'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'police_incidents',
        sa.Column('cad_call_number', sa.types.CHAR(length=25)),
        sa.Column('incident_number', sa.types.CHAR(length=25)),
        sa.Column('call_datetime', sa.DateTime(timezone=True)),
        sa.Column('x_coordinate', sa.types.CHAR(length=7)),
        sa.Column('y_coordinate', sa.types.CHAR(length=7)),
        sa.Column('incident_address', sa.types.CHAR(length=256)),
        sa.Column('street_number', sa.types.CHAR(length=10)),
        sa.Column('street_prefix', sa.types.CHAR(length=30)),
        sa.Column('street_name', sa.types.CHAR(length=200)),
        sa.Column('street_type', sa.types.CHAR(length=20)),
        sa.Column('street_suffix', sa.types.CHAR(length=20)),
        sa.Column('street_zip', sa.types.CHAR(length=20)),

        sa.Column('initial_cad_call_type', sa.types.CHAR(length=20)),
        sa.Column('initial_cad_call_type_description', sa.types.CHAR(length=100)),
        sa.Column('final_cad_call_type', sa.types.CHAR(length=20)),
        sa.Column('final_cad_call_type_description', sa.types.CHAR(length=100))
    )


def downgrade():
    op.drop_table('police_incidents')
    pass
