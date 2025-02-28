"""empty message

Revision ID: e7ec7f27694b
Revises: 
Create Date: 2022-07-12 01:54:13.532079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7ec7f27694b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('categories')
    op.drop_table('questions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('question', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('answer', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('difficulty', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('category', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category'], ['categories.id'], name='category', onupdate='CASCADE', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name='questions_pkey')
    )
    op.create_table('categories',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('type', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='categories_pkey')
    )
    # ### end Alembic commands ###
