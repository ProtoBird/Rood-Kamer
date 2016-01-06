"""Changed various user and role properties

Revision ID: 0e923b42f8b0
Revises: f91c2e507fa
Create Date: 2016-01-06 13:26:36.260943

"""

# revision identifiers, used by Alembic.
revision = '0e923b42f8b0'
down_revision = 'f91c2e507fa'

from alembic import op

from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('roles', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'roles', 'users', ['user_id'], ['id'])
    op.drop_constraint(u'users_ibfk_1', 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')


def downgrade():
    op.add_column('users', sa.Column('role_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'users_ibfk_1', 'users', 'roles', ['role_id'], ['id'])
    op.drop_constraint(None, 'roles', type_='foreignkey')
    op.drop_column('roles', 'user_id')
