from aiogram import Router
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka import FromDishka

from application.interactors import GetAllDishByTypeInteractor, DeleteDishInteractor
from domain.entities import DishType

router = Router()


class DeleteDishStates(StatesGroup):
    choosing_type = State()
    viewing_page = State()


def type_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завтрак", callback_data="delete_type_breakfast"
                ),
                InlineKeyboardButton(text="Обед", callback_data="delete_type_lunch"),
                InlineKeyboardButton(text="Ужин", callback_data="delete_type_dinner"),
            ]
        ]
    )


def pagination_keyboard(page: int, has_next: bool) -> InlineKeyboardMarkup:
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page - 1}"))
    if has_next:
        buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{page + 1}"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@router.message(lambda msg: msg.text == "Удалить блюдо")
async def handle_delete_dish_start(message: Message, state: FSMContext) -> None:
    """Начало процесса удаления блюда."""
    await message.answer(
        "Выберите тип блюда для удаления:", reply_markup=type_keyboard()
    )
    await state.set_state(DeleteDishStates.choosing_type)


@router.callback_query(lambda c: c.data.startswith("delete_type_"))
async def handle_choose_dish_type(
    callback: CallbackQuery,
    state: FSMContext,
    read_all_by_dish_type_interactor: FromDishka[GetAllDishByTypeInteractor],
) -> None:
    """Обработка выбора типа блюда."""
    dish_type = getattr(DishType, callback.data.split("_")[2]).value

    await state.update_data(dish_type=dish_type, page=0)
    await callback.message.delete()

    await send_dish_list(
        callback.message,
        dish_type=dish_type,
        page=0,
        read_all_by_dish_type_interactor=read_all_by_dish_type_interactor,
    )
    await state.set_state(DeleteDishStates.viewing_page)
    await callback.answer()


async def send_dish_list(
    message: Message | CallbackQuery,
    dish_type: str,
    page: int,
    read_all_by_dish_type_interactor: FromDishka[GetAllDishByTypeInteractor],
) -> None:
    """Отправляет список блюд с учётом пагинации."""
    dishes_per_page = 5
    offset = page * dishes_per_page
    owner=message.chat.id if isinstance(message, Message) else message.message.chat.id

    dishes = await read_all_by_dish_type_interactor(
        dish_type=dish_type, offset=offset, limit=dishes_per_page, owner=owner
    )

    if not dishes:
        await message.answer("Нет блюд для отображения.")
        return

    has_next = len(dishes) == dishes_per_page

    dish_list = "\n".join(
        f"{index + 1 + offset}. {dish.name} (Вес: {dish.random_weight})"
        for index, dish in enumerate(dishes)
    )

    buttons = [
        [
            InlineKeyboardButton(
                text=f"Удалить {dish.name}", callback_data=f"delete_{dish.uuid}"
            )
        ]
        for dish in dishes
    ]

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"page_{page - 1}")
        )
    if has_next:
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=f"page_{page + 1}")
        )

    if pagination_buttons:
        buttons.append(pagination_buttons)

    buttons.append(
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="close_pagination")]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    text = f"Блюда ({dish_type.capitalize()}):\n\n{dish_list}"
    if isinstance(message, CallbackQuery):
        await message.message.edit_text(text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("delete_"))
async def handle_delete_dish(
    callback: CallbackQuery,
    delete_dish_interactor: FromDishka[DeleteDishInteractor],
    state: FSMContext,
    read_all_by_dish_type_interactor: FromDishka[GetAllDishByTypeInteractor],
) -> None:
    """Обработка кнопки удаления блюда."""
    dish_uuid = callback.data.split("_")[1]

    try:
        await delete_dish_interactor(uuid=dish_uuid, owner=callback.message.chat.id)
        await callback.answer("Блюдо удалено.")

        data = await state.get_data()
        dish_type = data.get("dish_type")
        page = data.get("page", 0)

        await send_dish_list(
            callback, dish_type, page, read_all_by_dish_type_interactor
        )
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")


@router.callback_query(lambda c: c.data.startswith("page_"))
async def handle_pagination(
    callback: CallbackQuery,
    state: FSMContext,
    get_dishes_interactor: FromDishka[GetAllDishByTypeInteractor],
) -> None:
    """Обработка кнопок пагинации."""
    page = int(callback.data.split("_")[1])
    data = await state.get_data()
    dish_type = data.get("dish_type")

    await send_dish_list(callback, dish_type, page, get_dishes_interactor)
    await state.update_data(page=page)
    await callback.answer()


@router.callback_query(lambda callback: callback.data == "close_pagination")
async def handle_close_pagination(callback: CallbackQuery):
    """Удаляет сообщение с пагинацией."""
    await callback.message.delete()
