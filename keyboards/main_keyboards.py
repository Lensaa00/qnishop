from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 1
    keyboard.row(
        InlineKeyboardButton(
            text="🛒 Каталог",
            callback_data="catalog"
        ),
        InlineKeyboardButton(
            text="👤 Профиль",
            callback_data="profile"
        ),
    )
    return keyboard.as_markup()

def catalog_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 2

    keyboard.row(
        InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data="start_callback"
        )
    )
    return keyboard.as_markup()


def profile_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 1
    keyboard.row(
        InlineKeyboardButton(
            text="💸 Пополнить баланс",
            callback_data="deposit_balance"
        ),
        InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data="start_callback"
        )
    )
    return keyboard.as_markup()

