"""empty message

Revision ID: 93276358d306
Revises: 4dd52db15c65
Create Date: 2022-08-19 20:23:36.581220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93276358d306'
down_revision = '4dd52db15c65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('gold', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'gold')
    # ### end Alembic commands ###