"""update business licenses

Revision ID: 1581ef0e0d30
Revises: 1bab55c1377a
Create Date: 2014-07-22 15:55:32.487870

"""

# revision identifiers, used by Alembic.
revision = '1581ef0e0d30'
down_revision = '1bab55c1377a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('business_licenses', 'all_business_licenses')
    op.alter_column('all_business_licenses', 
                    'name',
                    type_=sa.types.CHAR(length=200))

    op.alter_column('all_business_licenses', 
                    'business_class',
                    type_=sa.types.CHAR(length=40))
    op.alter_column('all_business_licenses', 
                    'business_service_description',
                    type_=sa.types.CHAR(length=100))
    op.alter_column('all_business_licenses', 
                    'business_product',
                    type_=sa.types.CHAR(length=40))
    op.alter_column('all_business_licenses', 
                    'business_address',
                    type_=sa.types.CHAR(length=200))

    op.add_column('all_business_licenses', 
            sa.Column('business_street_number', 
                    sa.types.CHAR(length=10)))
    op.add_column('all_business_licenses', 
            sa.Column('business_street_prefix',
                    sa.types.CHAR(length=30)))
    op.add_column('all_business_licenses', 
            sa.Column('business_street_name',
                    sa.types.CHAR(length=200)))
    op.add_column('all_business_licenses', 
            sa.Column('business_street_type',
                    sa.types.CHAR(length=20)))
    op.add_column('all_business_licenses', 
            sa.Column('business_street_suffix',
                    sa.types.CHAR(length=20)))
#    op.alter_column('all_business_licenses',
#                    'business_zip',
#                    type_=sa.types.CHAR(length=20))
    op.add_column('all_business_licenses', 
            sa.Column('business_zip',
                    sa.types.CHAR(length=20)))


def downgrade():
    op.rename_table('all_business_licenses', 'business_licenses')
    op.alter_column('all_business_licenses', 
                    'name',
                    type_=sa.types.VARCHAR(length=200))

    op.alter_column('all_business_licenses', 
                    'business_class',
                    type_=sa.types.VARCHAR(length=40))
    op.alter_column('all_business_licenses', 
                    'business_service_description',
                    type_=sa.types.VARCHAR(length=100))
    op.alter_column('all_business_licenses', 
                    'business_product',
                    type_=sa.types.VARCHAR(length=40))
    op.alter_column('all_business_licenses', 
                    'business_address',
                    type_=sa.types.VARCHAR(length=200))
    op.alter_column('all_business_licenses',
                    'business_zip',
                    type_=sa.types.VARCHAR(length=20))

    op.drop_column('all_business_licenses', 'business_street_number')
    op.drop_column('all_business_licenses', 'business_street_prefix')
    op.drop_column('all_business_licenses', 'business_street_name')
    op.drop_column('all_business_licenses', 'business_street_type')
    op.drop_column('all_business_licenses', 'business_street_suffix')
    op.drop_column('all_business_licenses', 'business_zip')
