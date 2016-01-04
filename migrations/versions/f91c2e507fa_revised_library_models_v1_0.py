"""revised library models v1.0

Revision ID: f91c2e507fa
Revises: 23be4615053f
Create Date: 2016-01-04 10:35:48.514493

"""

# revision identifiers, used by Alembic.
revision = 'f91c2e507fa'
down_revision = '23be4615053f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('library_authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publishers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('isDeadTree', sa.Boolean(), nullable=False),
    sa.Column('pages', sa.Integer(), nullable=True),
    sa.Column('bookType', sa.String(length=64), nullable=False),
    sa.Column('publicationDate', sa.DateTime(), nullable=True),
    sa.Column('originalPublicationDate', sa.DateTime(), nullable=True),
    sa.Column('publishedBy', sa.Integer(), nullable=True),
    sa.Column('isbn', sa.String(length=10), nullable=True),
    sa.Column('isbn13', sa.String(length=13), nullable=True),
    sa.ForeignKeyConstraint(['publishedBy'], ['publishers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn'),
    sa.UniqueConstraint('isbn13')
    )
    op.create_table('authors_to_books',
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['library_authors.id'], ),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], )
    )
    op.add_column(u'users', sa.Column('books_checked_out', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'books', ['books_checked_out'], ['id'])
    ### end Alembic commands ###


def downgrade():
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column(u'users', 'books_checked_out')
    op.drop_table('authors_to_books')
    op.drop_table('books')
    op.drop_table('publishers')
    op.drop_table('library_authors')
