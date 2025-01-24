from random import choices

from application import interfaces
from application.dto import NewDishDTO
from domain import entities


class GetDishInteractor:
    def __init__(
        self,
        dish_gateway: interfaces.DishReader,
    ) -> None:
        self._dish_gateway = dish_gateway

    async def __call__(self, uuid: str) -> entities.DishDM | None:
        return await self._dish_gateway.read_by_uuid(uuid)


class GetAllDishInteractor:
    def __init__(
        self,
        dish_gateway: interfaces.DishReader,
    ) -> None:
        self._dish_gateway = dish_gateway

    async def __call__(self) -> list[entities.DishDM] | None:
        return await self._dish_gateway.read_all()


class NewDishInteractor:
    def __init__(
        self,
        db_session: interfaces.DBSession,
        dish_gateway: interfaces.DishSaver,
        uuid_generator: interfaces.UUIDGenerator,
    ) -> None:
        self._db_session = db_session
        self._dish_gateway = dish_gateway
        self._uuid_generator = uuid_generator

    async def __call__(self, dto: NewDishDTO) -> str:
        uuid = str(self._uuid_generator())
        dish = entities.DishDM(
            uuid=uuid,
            name=dto.name,
            random_weight=dto.random_weight,
        )

        await self._dish_gateway.save(dish)
        await self._db_session.commit()
        return uuid

class GenerateMenuInteractor:
    def __init__(
            self,
            dish_gateway: interfaces.DishReader,
    ) -> None:
        self._dish_gateway = dish_gateway

    async def __call__ (self, period: int) -> dict[str, entities.DishDM]:
        dishes = await self._dish_gateway.read_all()
        if len(dishes) < period:
            raise ValueError(f'Недостаточно блюд для составления меню на {period} дней')

        available_dishes = dishes.copy()
        menu = {}

        for day_number in range(1, period + 1):
            weights = [dish.random_weight for dish in available_dishes]
            selected_dish = choices(available_dishes, weights=weights, k=1)[0]

            menu[f"День {day_number}"] = selected_dish
            available_dishes.remove(selected_dish)

        return menu