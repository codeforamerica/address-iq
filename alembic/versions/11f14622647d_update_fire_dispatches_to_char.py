"""update fire and business tables

Revision ID: 11f14622647d
Revises: 21498b737579
Create Date: 2014-07-22 12:37:44.615688

"""

# revision identifiers, used by Alembic.
revision = '11f14622647d'
down_revision = '21498b737579'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Varchar => char in dispatches
    op.alter_column('fire_dispatches', 
                    'apparatus_id',
                    type_=sa.types.CHAR(length=6))
    
    op.alter_column('fire_dispatches', 
                    'apparatus_type',
                    type_=sa.types.CHAR(length=3))

    op.alter_column('fire_dispatches', 
                    'apparatus_description',
                    type_=sa.types.CHAR(length=100))

    op.alter_column('fire_dispatches', 
                    'dispatch_datetime',
                    type_=sa.types.CHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'enroute_scene_datetime',
                    type_=sa.types.CHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'arrival_datetime',
                    type_=sa.types.CHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'depart_scene_datetime',
                    type_=sa.types.CHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'arrived_facility_datetime',
                    type_=sa.types.CHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'clear_datetime',
                    type_=sa.types.CHAR(length=30))

def downgrade():
    op.alter_column('fire_dispatches', 
                    'apparatus_id',
                    type_=sa.types.VARCHAR(length=6))
    
    op.alter_column('fire_dispatches', 
                    'apparatus_type',
                    type_=sa.types.VARCHAR(length=3))

    op.alter_column('fire_dispatches', 
                    'apparatus_description',
                    type_=sa.types.VARCHAR(length=100))

    op.alter_column('fire_dispatches', 
                    'dispatch_datetime',
                    type_=sa.types.VARCHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'enroute_scene_datetime',
                    type_=sa.types.VARCHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'arrival_datetime',
                    type_=sa.types.VARCHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'depart_scene_datetime',
                    type_=sa.types.VARCHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'arrived_facility_datetime',
                    type_=sa.types.VARCHAR(length=30))
    op.alter_column('fire_dispatches', 
                    'clear_datetime',
                    type_=sa.types.VARCHAR(length=30))
