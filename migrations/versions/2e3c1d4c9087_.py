"""empty message

Revision ID: 2e3c1d4c9087
Revises: 46735a4df9e7
Create Date: 2022-08-17 16:07:28.712776

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2e3c1d4c9087'
down_revision = '46735a4df9e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'phone',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('user', 'role',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('user', 'avatar',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('user', 'description',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('user', 'join_time',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'join_time',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('user', 'description',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('user', 'avatar',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('user', 'role',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('user', 'phone',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###