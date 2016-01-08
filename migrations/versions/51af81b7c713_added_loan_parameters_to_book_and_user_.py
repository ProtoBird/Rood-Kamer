"""Added loan parameters to book and user models

Revision ID: 51af81b7c713
Revises: 0e923b42f8b0
Create Date: 2016-01-08 18:02:10.576204

"""

# revision identifiers, used by Alembic.
revision = '51af81b7c713'
down_revision = '0e923b42f8b0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('books', sa.Column('conditionOfLoan', sa.Text(), nullable=True))
    op.add_column('books', sa.Column('loaned_id', sa.Integer(), nullable=True))
    op.add_column('books', sa.Column('possession_id', sa.Integer(), nullable=True))
    op.add_column('books', sa.Column('termOfLoan', sa.Date(), nullable=True))
    op.create_foreign_key(u'books_ibfk_2', 'books', 'users', ['loaned_id'], ['id'])
    op.create_foreign_key(u'books_ibfk_3', 'books', 'users', ['possession_id'], ['id'])
    op.drop_constraint(u'users_ibfk_2', 'users', type_='foreignkey')
    op.drop_column('users', 'books_loaned')
    op.drop_column('users', 'books_checked_out')


def downgrade():
    op.add_column('users', sa.Column('books_checked_out', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('books_loaned', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_foreign_key(u'users_ibfk_2', 'users', 'books', ['books_checked_out'], ['id'])
    op.drop_constraint(u'books_ibfk_2', 'books', type_='foreignkey')
    op.drop_constraint(u'books_ibfk_3', 'books', type_='foreignkey')
    op.drop_column('books', 'termOfLoan')
    op.drop_column('books', 'possession_id')
    op.drop_column('books', 'loaned_id')
    op.drop_column('books', 'conditionOfLoan')
