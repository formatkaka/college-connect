"""empty message

Revision ID: 3ffc786ed329
Revises: 61a8dec163da
Create Date: 2016-02-10 17:09:20.533000

"""

# revision identifiers, used by Alembic.
revision = '3ffc786ed329'
down_revision = '61a8dec163da'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('metaData', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'metaData')
    ### end Alembic commands ###
