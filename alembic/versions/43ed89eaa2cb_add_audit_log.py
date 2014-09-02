"""add audit log

Revision ID: 43ed89eaa2cb
Revises: 5932c01014d4
Create Date: 2014-08-21 14:05:51.120546

"""

# revision identifiers, used by Alembic.
revision = '43ed89eaa2cb'
down_revision = '4edfa46798f8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'audit_log',
        sa.Column('timestamp', sa.DateTime(timezone=True)),
        sa.Column('resource', sa.String(100)),
        sa.Column('method', sa.String(10)),
        sa.Column('response_code', sa.String(3)),
        sa.Column('user_id', sa.String(8))
    )


def downgrade():
    op.drop_table('audit_log')
