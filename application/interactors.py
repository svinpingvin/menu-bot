from random import choices
from typing import Optional

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


class GetAllDishByTypeInteractor:
    def __init__(
        self,
        dish_gateway: interfaces.DishReader,
    ) -> None:
        self._dish_gateway = dish_gateway

    async def __call__(
        self, dish_type: str = None, offset: int = 0, limit: int = 5
    ) -> list[entities.DishDM] | None:
        return await self._dish_gateway.read_all_by_dish_type(
            dish_type=dish_type, offset=offset, limit=limit
        )


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
            dish_type=dto.dish_type,
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

    async def __call__(
        self, period: int
    ) -> dict[str, dict[str, Optional[entities.DishDM]]]:
        """Генерация меню с учётом всех типов блюд."""

        dishes = await self._dish_gateway.read_all()

        dishes_by_type = {
            dish_type.value: [
                dish for dish in dishes if dish.dish_type == dish_type.value
            ]
            for dish_type in entities.DishType.__members__.values()
        }

        for dish_type, dish_list in dishes_by_type.items():
            if not dish_list:
                dishes_by_type[dish_type] = None

        menu = {}

        for day_number in range(1, period + 1):
            daily_menu = {}

            for dish_type, dish_list in dishes_by_type.items():
                if not dish_list:
                    daily_menu[dish_type.capitalize()] = "-"
                else:
                    weights = [dish.random_weight for dish in dish_list]
                    selected_dish = choices(dish_list, weights=weights, k=1)[0]
                    daily_menu[dish_type.capitalize()] = selected_dish

                    dish_list.remove(selected_dish)

                    if not dish_list:
                        dishes_by_type[dish_type] = None

            menu[f"День {day_number}"] = daily_menu

        return menu


class DeleteDishInteractor:
    def __init__(
        self,
        dish_gateway: interfaces.DishRemover,
    ) -> None:
        self._dish_gateway = dish_gateway

    async def __call__(self, uuid: str) -> None:
        return await self._dish_gateway.remove_by_uuid(uuid)
