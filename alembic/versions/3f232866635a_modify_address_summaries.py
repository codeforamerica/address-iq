"""modify address_summaries

Revision ID: 3f232866635a
Revises: 1ee76cf990d9
Create Date: 2014-09-06 13:26:25.239336

"""

# revision identifiers, used by Alembic.
revision = '3f232866635a'
down_revision = '1ee76cf990d9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('address_summaries', 'business_counts', new_column_name='business_count')
    op.add_column('address_summaries', sa.Column('active', sa.Boolean))


def downgrade():
    op.alter_column('address_summaries', 'business_count', new_column_name='business_counts')
    op.drop_column('address_summaries', 'active')
