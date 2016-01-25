"""empty message

Revision ID: c1dcbefacda5
Revises: 4adc1bc7a3af
Create Date: 2016-01-25 17:55:10.939000

"""

# revision identifiers, used by Alembic.
revision = 'c1dcbefacda5'
down_revision = '4adc1bc7a3af'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'users_userName_key', 'users', type_='unique')
    op.drop_column('users', 'userName')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('userName', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint(u'users_userName_key', 'users', ['userName'])
    ### end Alembic commands ###