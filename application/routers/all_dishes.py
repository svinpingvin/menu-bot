from aiogram import Router
from aiogram.types import Message
from dishka import FromDishka

from application.interactors import GetAllDishInteractor

router = Router()


@router.message(lambda msg: msg.text == "Список блюд")
async def handle_all_dishes(
    message: Message,
    get_all_dish_interactor: FromDishka[GetAllDishInteractor],
) -> None:
    """Обработка команды 'Список блюд'. Показывает все блюда, сгруппированные по типам."""
    try:
        all_dishes = await get_all_dish_interactor(owner=message.chat.id)
        if not all_dishes:
            await message.answer("Список блюд пуст.")
            return

        # Группируем блюда по типам
        grouped_dishes = {
            "Завтрак": [],
            "Обед": [],
            "Ужин": [],
        }
        for dish in all_dishes:
            grouped_dishes[dish.dish_type].append(dish)

        # Формируем текст ответа
        response_parts = []
        for dish_type, dishes in grouped_dishes.items():
            if dishes:
                dish_list = "\n".join(
                    f"{index + 1}. {dish.name} (Вес: {dish.random_weight})"
                    for index, dish in enumerate(dishes)
                )
                response_parts.append(f"**{dish_type}:**\n{dish_list}")

        response_text = "\n\n".join(response_parts)
        await message.answer(response_text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
