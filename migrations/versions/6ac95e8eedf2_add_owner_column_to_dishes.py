"""Add owner column to dishes

Revision ID: 6ac95e8eedf2
Revises: 8ec6c90fd6ad
Create Date: 2025-01-26 09:57:57.217848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ac95e8eedf2'
down_revision: Union[str, None] = '8ec6c90fd6ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dishes', sa.Column('owner', sa.Integer(), nullable=False, server_default="0"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dishes', 'owner')
    # ### end Alembic commands ###
