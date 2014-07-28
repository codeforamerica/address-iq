"""fix nfirs description length

Revision ID: 4ca6c04c18de
Revises: 267c21e1267b
Create Date: 2014-07-22 18:25:36.440237

"""

# revision identifiers, used by Alembic.
revision = '4ca6c04c18de'
down_revision = '267c21e1267b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('fire_incidents', 
                    'actual_nfirs_incident_type_description',
                    type_=sa.types.CHAR(length=100))
    op.alter_column('fire_incidents', 
                    'intersection',
                    type_=sa.types.CHAR(length=200))

def downgrade():
    op.alter_column('fire_incidents', 
                    'actual_nfirs_incident_type_description',
                    type_=sa.types.CHAR(length=6))
    op.alter_column('fire_incidents', 
                    'intersection',
                    type_=sa.types.CHAR(length=6))
