"""Add dish_type column to dishes

Revision ID: 8ec6c90fd6ad
Revises: 0c3eafd9f60b
Create Date: 2025-01-25 20:38:59.522011

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "8ec6c90fd6ad"
down_revision: Union[str, None] = "0c3eafd9f60b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    dish_type_enum = postgresql.ENUM("Завтрак", "Обед", "Ужин", name="dish_type_enum")
    dish_type_enum.create(op.get_bind())

    op.add_column(
        "dishes",
        sa.Column("dish_type", dish_type_enum, nullable=False, server_default="Ужин"),
    )


def downgrade() -> None:
    op.drop_column("dishes", "dish_type")
    dish_type_enum = postgresql.ENUM("Завтрак", "Обед", "Ужин", name="dish_type_enum")
    dish_type_enum.drop(op.get_bind())  # Удаляет ENUM из базы данных
