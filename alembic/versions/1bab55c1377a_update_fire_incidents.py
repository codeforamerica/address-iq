"""update fire incidents

Revision ID: 1bab55c1377a
Revises: 11f14622647d
Create Date: 2014-07-22 15:40:47.683518

"""

# revision identifiers, used by Alembic.
revision = '1bab55c1377a'
down_revision = '11f14622647d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('fire_incidents', 
                    'district',
                    type_=sa.types.CHAR(length=6))

    op.alter_column('fire_incidents', 
                    'x_coordinate',
                    type_=sa.types.CHAR(length=7))
    op.alter_column('fire_incidents', 
                    'y_coordinate',
                    type_=sa.types.CHAR(length=7))

    op.alter_column('fire_incidents', 
                    'street_number',
                    type_=sa.types.CHAR(length=10))
    op.alter_column('fire_incidents', 
                    'street_prefix',
                    type_=sa.types.CHAR(length=30))
    op.alter_column('fire_incidents', 
                    'street_name',
                    type_=sa.types.CHAR(length=200))
    op.alter_column('fire_incidents', 
                    'street_type',
                    type_=sa.types.CHAR(length=20))
    op.alter_column('fire_incidents', 
                    'street_suffix',
                    type_=sa.types.CHAR(length=20))

    op.alter_column('fire_incidents', 
                    'cross_street_prefix',
                    type_=sa.types.CHAR(length=30))
    op.alter_column('fire_incidents', 
                    'cross_street_name',
                    type_=sa.types.CHAR(length=200))
    op.alter_column('fire_incidents', 
                    'cross_street_type',
                    type_=sa.types.CHAR(length=20))
    op.alter_column('fire_incidents', 
                    'cross_street_suffix',
                    type_=sa.types.CHAR(length=20))

    op.alter_column('fire_incidents', 
                    'incident_address',
                    type_=sa.types.CHAR(length=255))
    op.alter_column('fire_incidents', 
                    'apartment_number',
                    type_=sa.types.CHAR(length=20))
    op.alter_column('fire_incidents', 
                    'incident_cross_street',
                    type_=sa.types.CHAR(length=255))

    op.alter_column('fire_incidents', 
                    'postal_code',
                    type_=sa.types.CHAR(length=10))
    op.alter_column('fire_incidents', 
                    'common_name',
                    type_=sa.types.CHAR(length=200))

    op.alter_column('fire_incidents', 
                    'initial_cad_call_type',
                    type_=sa.types.CHAR(length=20))
    op.alter_column('fire_incidents', 
                    'initial_cad_call_type_description',
                    type_=sa.types.CHAR(length=100))
    
    op.alter_column('fire_incidents', 
                    'final_cad_call_type',
                    type_=sa.types.CHAR(length=20))
    op.alter_column('fire_incidents', 
                    'final_cad_call_type_description',
                    type_=sa.types.CHAR(length=100))

    op.alter_column('fire_incidents', 
                    'actual_nfirs_incident_type',
                    type_=sa.types.CHAR(length=20))
    op.alter_column('fire_incidents', 
                    'actual_nfirs_incident_type_description',
                    type_=sa.types.CHAR(length=6))
    op.alter_column('fire_incidents', 
                    'intersection',
                    type_=sa.types.CHAR(length=6))

def downgrade():
    op.alter_column('fire_incidents', 
                    'district',
                    type_=sa.types.VARCHAR(length=6))

    op.alter_column('fire_incidents', 
                    'x_coordinate',
                    type_=sa.types.VARCHAR(length=7))
    op.alter_column('fire_incidents', 
                    'y_coordinate',
                    type_=sa.types.VARCHAR(length=7))

    op.alter_column('fire_incidents', 
                    'street_number',
                    type_=sa.types.VARCHAR(length=10))
    op.alter_column('fire_incidents', 
                    'street_prefix',
                    type_=sa.types.VARCHAR(length=30))
    op.alter_column('fire_incidents', 
                    'street_name',
                    type_=sa.types.VARCHAR(length=200))
    op.alter_column('fire_incidents', 
                    'street_type',
                    type_=sa.types.VARCHAR(length=20))
    op.alter_column('fire_incidents', 
                    'street_suffix',
                    type_=sa.types.VARCHAR(length=20))

    op.alter_column('fire_incidents', 
                    'cross_street_prefix',
                    type_=sa.types.VARCHAR(length=30))
    op.alter_column('fire_incidents', 
                    'cross_street_name',
                    type_=sa.types.VARCHAR(length=200))
    op.alter_column('fire_incidents', 
                    'cross_street_type',
                    type_=sa.types.VARCHAR(length=20))
    op.alter_column('fire_incidents', 
                    'cross_street_suffix',
                    type_=sa.types.VARCHAR(length=20))

    op.alter_column('fire_incidents', 
                    'incident_address',
                    type_=sa.types.VARCHAR(length=255))
    op.alter_column('fire_incidents', 
                    'apartment_number',
                    type_=sa.types.VARCHAR(length=20))
    op.alter_column('fire_incidents', 
                    'incident_cross_street',
                    type_=sa.types.VARCHAR(length=255))

    op.alter_column('fire_incidents', 
                    'postal_code',
                    type_=sa.types.VARCHAR(length=10))
    op.alter_column('fire_incidents', 
                    'common_name',
                    type_=sa.types.VARCHAR(length=200))

    op.alter_column('fire_incidents', 
                    'initial_cad_call_type',
                    type_=sa.types.VARCHAR(length=20))
    op.alter_column('fire_incidents', 
                    'initial_cad_call_type_description',
                    type_=sa.types.VARCHAR(length=100))
    
    op.alter_column('fire_incidents', 
                    'final_cad_call_type',
                    type_=sa.types.VARCHAR(length=20))
    op.alter_column('fire_incidents', 
                    'final_cad_call_type_description',
                    type_=sa.types.VARCHAR(length=100))

    op.alter_column('fire_incidents', 
                    'actual_nfirs_incident_type',
                    type_=sa.types.VARCHAR(length=20))
    op.alter_column('fire_incidents', 
                    'actual_nfirs_incident_type_description',
                    type_=sa.types.VARCHAR(length=6))
    op.alter_column('fire_incidents', 
                    'intersection',
                    type_=sa.types.VARCHAR(length=6))
