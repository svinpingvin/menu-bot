from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from dishka import FromDishka

from application.dto import NewDishDTO
from application.interactors import (
    NewDishInteractor,
    GetAllDishInteractor, GenerateMenuInteractor,
)

router = Router()


@router.message(Command("start"))
async def handle_start(message: Message) -> None:
    """Обработчик команды /start."""
    await message.answer("Привет! Я бот для составления меню ужинов на 2 недели.")


@router.message(Command("add_dish"))
async def handle_add_dish(
    message: Message, create_new_dish_interactor: FromDishka[NewDishInteractor]
) -> None:
    """Обработчик команды /add_dish."""
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            raise ValueError("Неверный формат команды. Пример: /add_dish Паста 5")

        name, weight = parts[1], int(parts[2])
        dto = NewDishDTO(name=name, random_weight=weight)
        dish_uuid = await create_new_dish_interactor(dto)

        await message.answer(f"Блюдо '{name}' успешно добавлено! UUID: {dish_uuid}")
    except Exception:
        await message.answer("Ошибка")


@router.message(Command("all_dishes"))
async def handle_all_dishes(
    message: Message, get_all_dish_interactor: FromDishka[GetAllDishInteractor]
) -> None:
    """Обработчик команды /all_dishes."""
    try:
        all_dishes = await get_all_dish_interactor()
        answer = "Список блюд пуст"
        if all_dishes:
            answer = "\n".join(
                f"{index + 1}. {dish.name}, {dish.random_weight}"
                for index, dish in enumerate(all_dishes)
            )

        await message.answer(answer)

    except Exception:
        await message.answer("Ошибка")


@router.message(Command("generate_menu"))
async def handle_generate_menu(
    message: Message, generate_menu_interactor: FromDishka[GenerateMenuInteractor]
) -> None:
    """Обработчик команды /generate_menu."""
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) >= 2:
            period = int(parts[1])
        else:
            period = 14
            await message.answer('Период задан по умолчанию на 14 дней')
        menu = await generate_menu_interactor(period=period)
        answer = "\n\n".join(
            f"{day}:\n {dish.name}"
            for day, dish in menu.items()
        )

        await message.answer(f"Меню:\n\n{answer}")

    except ValueError as e:
        await message.answer(str(e))
