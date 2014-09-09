"""modify length in address summary


Revision ID: 43c6e3f2548a
Revises: 1ee76cf990d9
Create Date: 2014-09-08 22:58:12.130839

"""

# revision identifiers, used by Alembic.
revision = '43c6e3f2548a'
down_revision = '1ee76cf990d9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('address_summaries', 
                    'address',
                    type_=sa.String(200))


def downgrade():
    op.alter_column('address_summaries', 
                    'address',
                    type_=sa.String(50))
