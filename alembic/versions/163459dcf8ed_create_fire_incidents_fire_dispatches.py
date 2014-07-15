"""create fire_incidents, fire_dispatches

Revision ID: 163459dcf8ed
Revises: None
Create Date: 2014-07-14 23:28:28.654258

"""

# revision identifiers, used by Alembic.
revision = '163459dcf8ed'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'fire_incidents',
        sa.Column('cad_call_number', sa.Integer, primary_key=True),
        sa.Column('incident_number', sa.Integer),
        sa.Column('alarm_datetime', sa.DateTime(timezone=True)),

        sa.Column('district', sa.String(6)),
        sa.Column('x_coordinate', sa.String(7)),
        sa.Column('y_coordinate', sa.String(7)),

        sa.Column('street_number', sa.String(10)),
        sa.Column('street_prefix', sa.String(30)),
        sa.Column('street_name', sa.String(200)),
        sa.Column('street_type', sa.String(20)),
        sa.Column('street_suffix', sa.String(20)),

        sa.Column('cross_street_prefix', sa.String(30)),
        sa.Column('cross_street_name', sa.String(200)),
        sa.Column('cross_street_type', sa.String(20)),
        sa.Column('cross_street_suffix', sa.String(20)),

        sa.Column('incident_address', sa.String(255)),
        sa.Column('apartment_number', sa.String(20)),
        sa.Column('incident_cross_street', sa.String(255)),

        sa.Column('postal_code', sa.String(10)),
        sa.Column('common_name', sa.String(200)),

        sa.Column('initial_cad_call_type', sa.String(20)),
        sa.Column('initial_cad_call_type_description', sa.String(255)),

        sa.Column('final_cad_call_type', sa.String(20)),
        sa.Column('final_cad_call_type_description', sa.String(255)),

        sa.Column('actual_nfirs_incident_type', sa.String(20)),
        sa.Column('actual_nfirs_incident_type_description', sa.String(255)),

        sa.Column('intersection', sa.String(255))
    )

    op.create_table(
        'fire_dispatches',
        sa.Column('incident_number', sa.Integer),

        sa.Column('apparatus_id', sa.String(6)),
        sa.Column('apparatus_type', sa.String(3)),
        sa.Column('apparatus_description', sa.String(255)),

        sa.Column('dispatch_datetime', sa.String(100)),
        sa.Column('enroute_scene_datetime', sa.String(30)),
        sa.Column('arrival_datetime', sa.String(30)),
        sa.Column('depart_scene_datetime', sa.String(30)),
        sa.Column('arrived_facility_datetime', sa.String(30)),
        sa.Column('clear_datetime', sa.String(30)),

        sa.Column('turnout_time_in_sec', sa.Integer),
        sa.Column('travel_time_nfpa_response_time_in_sec', sa.Integer),
        sa.Column('response_time_in_sec', sa.Integer),
        sa.Column('total_response_time_in_sec', sa.Integer),
        sa.Column('on_scene_time_where_transport_in_sec', sa.Integer),
        sa.Column('total_on_scene_time_with_or_without_transport_in_sec', sa.Integer),
        sa.Column('transport_time_in_sec', sa.Integer),
        sa.Column('turnaround_time_in_sec', sa.Integer),
        sa.Column('duration_time_in_sec', sa.Integer)
    )


def downgrade():
    op.drop_table('fire_incidents')
    op.drop_table('fire_dispatches')
