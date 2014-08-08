"""add users table

Revision ID: 355b87c794cf
Revises: 4ca6c04c18de
Create Date: 2014-08-08 11:12:31.906606

"""

# revision identifiers, used by Alembic.
revision = '355b87c794cf'
down_revision = '4ca6c04c18de'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(75)),
        sa.Column('email', sa.String(100), unique=True),
        sa.Column('date_created', sa.DateTime(timezone=True))
    )


def downgrade():
    op.drop_table('users')
