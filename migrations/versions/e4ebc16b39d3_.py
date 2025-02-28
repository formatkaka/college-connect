"""empty message

Revision ID: e4ebc16b39d3
Revises: 435f3e06c40d
Create Date: 2016-02-11 15:14:56.279000

"""

# revision identifiers, used by Alembic.
revision = 'e4ebc16b39d3'
down_revision = '435f3e06c40d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts_events', sa.Column('contactNumber', sa.String(), nullable=True))
    op.drop_column('contacts_events', 'contactNumbejhr')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts_events', sa.Column('contactNumbejhr', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('contacts_events', 'contactNumber')
    ### end Alembic commands ###
