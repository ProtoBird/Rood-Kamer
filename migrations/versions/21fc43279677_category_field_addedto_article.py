"""category field addedto article

Revision ID: 21fc43279677
Revises: 44869e10e39a
Create Date: 2015-04-17 18:04:18.299412

"""

# revision identifiers, used by Alembic.
revision = '21fc43279677'
down_revision = '44869e10e39a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('category', sa.String(length=80), nullable=True))
    op.create_unique_constraint(None, 'articles', ['category'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'articles')
    op.drop_column('articles', 'category')
    ### end Alembic commands ###
