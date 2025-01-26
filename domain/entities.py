from dataclasses import dataclass
from enum import StrEnum


class DishType(StrEnum):
    breakfast = "Завтрак"
    lunch = "Обед"
    dinner = "Ужин"


@dataclass(slots=True)
class DishDM:
    uuid: str
    name: str
    random_weight: int
    dish_type: str
    owner: int
