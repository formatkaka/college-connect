"""empty message

Revision ID: bfaec01a51a0
Revises: None
Create Date: 2016-01-23 13:51:55.386000

"""

# revision identifiers, used by Alembic.
revision = 'bfaec01a51a0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('dataa', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'test_pkey')
    )
    ### end Alembic commands ###
