import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from domain.entities import DishType

dish_type_enum = ENUM(
    *DishType.__members__.values(),
    name="dish_type_enum",
    create_type=True,
)


class Base(DeclarativeBase):
    pass


class Dish(Base):
    __tablename__ = "dishes"

    uuid: Mapped[str] = mapped_column(
        "uuid",
        sa.Uuid,
        primary_key=True,
    )
    name: Mapped[str]
    random_weight: Mapped[int]
    dish_type: Mapped[str] = mapped_column(dish_type_enum, nullable=False)
    owner: Mapped[int] = mapped_column(nullable=False)
