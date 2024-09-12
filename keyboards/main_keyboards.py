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


def catalog_keyboard(categories):
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 2
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category[1],
                callback_data=f"category_open_{category[0]}"
            )
        )
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
            text="Реферальная ссылка",
            callback_data="get_referral_link"
        ),
        InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data="start_callback"
        )
    )
    return keyboard.as_markup()


def referral_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 1
    keyboard.row(
        InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data="start_callback"
        )
    )
    return keyboard.as_markup()
