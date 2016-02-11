"""empty message

Revision ID: 61a8dec163da
Revises: 294ff9583fee
Create Date: 2016-02-08 23:52:41.492000

"""

# revision identifiers, used by Alembic.
revision = '61a8dec163da'
down_revision = '294ff9583fee'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('createdTime', sa.DateTime(), nullable=True))
    op.drop_column('events', 'imageB64')
    op.drop_column('events', 'time_created')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('time_created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('events', sa.Column('imageB64', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('events', 'createdTime')
    ### end Alembic commands ###