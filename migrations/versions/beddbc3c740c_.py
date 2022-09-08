"""empty message

Revision ID: beddbc3c740c
Revises: 0a4e9cd854d0
Create Date: 2022-08-21 13:07:46.654264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beddbc3c740c'
down_revision = '0a4e9cd854d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('threereply',
    sa.Column('tid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('notlikes', sa.Integer(), nullable=True),
    sa.Column('reply_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['reply_id'], ['reply.rid'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('tid')
    )
    op.add_column('reply', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'reply', 'user', ['user_id'], ['uid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reply', type_='foreignkey')
    op.drop_column('reply', 'user_id')
    op.drop_table('threereply')
    # ### end Alembic commands ###