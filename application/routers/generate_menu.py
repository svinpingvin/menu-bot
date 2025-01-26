from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka import FromDishka

from application.interactors import GenerateMenuInteractor
from domain import entities

router = Router()


class GenerateMenuStates(StatesGroup):
    selecting_days = State()


def days_keyboard():
    """Клавиатура для выбора количества дней."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1 неделя", callback_data="days_7"),
                InlineKeyboardButton(text="2 недели", callback_data="days_14"),
                InlineKeyboardButton(text="3 недели", callback_data="days_21"),
                InlineKeyboardButton(text="4 недели", callback_data="days_28"),
            ]
        ]
    )


@router.message(lambda msg: msg.text == "Сгенерировать меню")
async def handle_generate_menu_start(message: Message, state: FSMContext) -> None:
    """Начало процесса генерации меню."""
    await message.answer(
        "На сколько дней сгенерировать меню?", reply_markup=days_keyboard()
    )
    await state.set_state(GenerateMenuStates.selecting_days)


@router.callback_query(lambda callback: callback.data.startswith("days_"))
async def handle_days_selection(
    callback, generate_menu_interactor: FromDishka[GenerateMenuInteractor]
) -> None:
    """Обработка выбора количества дней для генерации меню."""
    days = int(callback.data.split("_")[1])

    try:
        menu = await generate_menu_interactor(period=days, owner=callback.message.chat.id)
        formatted_menu = format_menu(menu)
        await callback.message.edit_text(
            f"Сгенерированное меню:\n\n{formatted_menu}", reply_markup=None
        )
    except Exception as e:
        await callback.message.edit_text(
            f"Ошибка при генерации меню: {e}", reply_markup=None
        )


def format_menu(menu: dict) -> str:
    """Форматирует меню для отправки пользователю."""
    result = []
    for day, dishes in menu.items():
        day_menu = [f"{day}:"]
        for meal_type, dish in dishes.items():
            dish_info = dish.name if isinstance(dish, entities.DishDM) else dish
            day_menu.append(f"  - {meal_type}: {dish_info}")
        result.append("\n".join(day_menu))
    return "\n\n".join(result)
