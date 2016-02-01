"""empty message

Revision ID: f5e49045ff75
Revises: 905064992630
Create Date: 2016-01-27 10:42:47.454000

"""

# revision identifiers, used by Alembic.
revision = 'f5e49045ff75'
down_revision = '905064992630'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'hostelName')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('hostelName', sa.VARCHAR(), autoincrement=False, nullable=True))
    ### end Alembic commands ###