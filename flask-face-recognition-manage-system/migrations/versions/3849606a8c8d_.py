"""empty message

Revision ID: 3849606a8c8d
Revises: a0bc1155a3a6
Create Date: 2021-04-23 15:28:13.646503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3849606a8c8d'
down_revision = 'a0bc1155a3a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('Name', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'Name')
    # ### end Alembic commands ###
