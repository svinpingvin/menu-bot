from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka import FromDishka

from application.dto import NewDishDTO
from application.interactors import NewDishInteractor
from domain.entities import DishType

router = Router()


class AddDishStates(StatesGroup):
    choosing_type = State()
    choosing_weight = State()
    entering_name = State()


def type_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завтрак", callback_data="add_type_breakfast"
                ),
                InlineKeyboardButton(text="Обед", callback_data="add_type_lunch"),
                InlineKeyboardButton(text="Ужин", callback_data="add_type_dinner"),
            ]
        ]
    )


def weight_keyboard():
    buttons = [
        InlineKeyboardButton(text=str(weight), callback_data=f"weight_{weight}")
        for weight in range(10, 110, 10)
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[buttons[i : i + 5] for i in range(0, len(buttons), 5)]
    )


@router.message(lambda msg: msg.text == "Добавить блюдо")
async def handle_add_dish_start(message: Message, state: FSMContext) -> None:
    await message.answer("Выберите тип блюда:", reply_markup=type_keyboard())
    await state.set_state(AddDishStates.choosing_type)


@router.callback_query(lambda c: c.data.startswith("add_type_"))
async def handle_choose_type(callback: CallbackQuery, state: FSMContext) -> None:
    dish_type = getattr(DishType, callback.data.split("_")[2]).value
    await state.update_data(dish_type=dish_type)
    await callback.message.answer(
        "Теперь выберите вес блюда:", reply_markup=weight_keyboard()
    )
    await state.set_state(AddDishStates.choosing_weight)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("weight_"))
async def handle_choose_weight(callback: CallbackQuery, state: FSMContext) -> None:
    weight = int(callback.data.split("_")[1])
    await state.update_data(weight=weight)
    await callback.message.answer("Введите название блюда:")
    await state.set_state(AddDishStates.entering_name)
    await callback.answer()


@router.message(StateFilter(AddDishStates.entering_name))
async def handle_enter_name(
    message: Message,
    state: FSMContext,
    create_new_dish_interactor: FromDishka[NewDishInteractor],
):
    dish_data = await state.get_data()
    dish_type = dish_data["dish_type"]
    weight = dish_data["weight"]
    name = message.text

    try:
        dto = NewDishDTO(name=name, random_weight=weight, dish_type=dish_type, owner=message.chat.id)
        await create_new_dish_interactor(dto)
        await message.answer(
            f"Блюдо '{name}' успешно добавлено как '{dish_type}' с весом {weight}.",
        )
    except Exception as e:
        await message.answer(f"Ошибка при добавлении блюда: {e}")
    await state.clear()
