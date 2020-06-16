"""add category

Revision ID: b65752223558
Revises: eb19bf814cb3
Create Date: 2020-06-15 15:02:19.939535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b65752223558'
down_revision = 'eb19bf814cb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogs', sa.Column('category', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blogs', 'category')
    # ### end Alembic commands ###
