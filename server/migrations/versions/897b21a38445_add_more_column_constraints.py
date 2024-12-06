"""add more column constraints

Revision ID: 897b21a38445
Revises: f2db2bd6796c
Create Date: 2024-12-04 14:39:06.054842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '897b21a38445'
down_revision = 'f2db2bd6796c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###