"""add roles table

Revision ID: 185f531a6df2
Revises: 1cb8decfac89
Create Date: 2014-08-29 17:15:45.116681

"""

# revision identifiers, used by Alembic.
revision = '185f531a6df2'
down_revision = '1cb8decfac89'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), unique=True),
        sa.Column('description', sa.String(100))
    )


def downgrade():
    op.drop_table('roles')
