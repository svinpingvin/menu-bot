from dataclasses import dataclass


@dataclass(slots=True)
class DishDM:
    uuid: str
    name: str
    random_weight: int
