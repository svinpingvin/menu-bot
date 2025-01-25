from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()


def main_menu():
    """Создает основное меню с кнопками."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить блюдо")],
            [KeyboardButton(text="Список блюд")],
            [KeyboardButton(text="Удалить блюдо")],
            [KeyboardButton(text="Сгенерировать меню")],
        ],
        resize_keyboard=True,
    )


@router.message(Command("start"))
async def handle_start(message: Message) -> None:
    """Обрабатывает команду /start и отображает главное меню."""
    await message.answer(
        "Привет! Я бот для составления меню. При добавлении блюда ты увидишь слово Вес. "
        "Вес - это мера любимости тобой блюда, чем выше вес, тем выше шанс его выпадения. Выберите действие:",
        reply_markup=main_menu(),
    )
