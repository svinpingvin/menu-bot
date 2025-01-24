from dataclasses import dataclass


@dataclass(slots=True)
class NewDishDTO:
    name: str
    random_weight: int
