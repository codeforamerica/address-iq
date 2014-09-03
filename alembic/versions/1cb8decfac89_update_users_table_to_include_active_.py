"""update users table to include active status and login info

Revision ID: 1cb8decfac89
Revises: 43ed89eaa2cb
Create Date: 2014-08-29 17:15:02.149325

"""

# revision identifiers, used by Alembic.
revision = '1cb8decfac89'
down_revision = '43ed89eaa2cb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('active', sa.Boolean))
    op.add_column('users', sa.Column('last_login_at', sa.DateTime(timezone=True)))
    op.add_column('users', sa.Column('current_login_at', sa.DateTime(timezone=True)))
    op.add_column('users', sa.Column('last_login_ip', sa.String(45)))
    op.add_column('users', sa.Column('current_login_ip', sa.String(45)))
    op.add_column('users', sa.Column('login_count', sa.Integer))


def downgrade():
    op.drop_column('users', 'active')
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'current_login_at')
    op.drop_column('users', 'last_login_ip')
    op.drop_column('users', 'current_login_ip')
    op.drop_column('users', 'login_count')
