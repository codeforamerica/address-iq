"""add actions table

Revision ID: 4edfa46798f8
Revises: 355b87c794cf
Create Date: 2014-08-18 14:34:17.157466

"""

# revision identifiers, used by Alembic.
revision = '4edfa46798f8'
down_revision = '355b87c794cf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'actions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', sa.String),
        sa.Column('type', sa.String),
        sa.Column('content', sa.Text),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('created', sa.DateTime(timezone=True))
    )


def downgrade():
    op.drop_table('actions')
