from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.database import requests as rq


def start():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 1
    keyboard.row(
        InlineKeyboardButton(
            text="📚 Каталог",
            callback_data="catalog"
        ),
        InlineKeyboardButton(
            text="👤 Профиль",
            callback_data="profile"
        )
    )
    return keyboard.as_markup()


async def catalog():
    categories = await rq.get_categories()

    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 2

    for category in categories:
        keyboard.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f"category_{category.id}"
        ))

    keyboard.row(
        InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data="start"
        )
    )
    return keyboard.as_markup()


async def items(category_id):
    items = await rq.get_items_by_category_id(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in items:
        keyboard.add(InlineKeyboardButton(
            text=f"{item.name} | {item.price} руб.",
            callback_data=f"item_{item.id}"
        ))

    keyboard.row(InlineKeyboardButton(text="Вернуться в каталог", callback_data="catalog"))

    return keyboard.as_markup()


def profile():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 1
    keyboard.add(
        InlineKeyboardButton(
            text="Пополнить баланс",
            callback_data="balance"
        ),
        InlineKeyboardButton(
            text="Реферальная ссылка",
            callback_data="get_referral"
        ),
        InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data="start"
        )
    )
    return keyboard.as_markup()


def deposit_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 2
    prices = [100, 200, 500, 1000]
    for price in prices:
        keyboard.add(InlineKeyboardButton(
            text=f"{price}руб.",
            callback_data=f"deposit_{price}"
        ))
    keyboard.row(InlineKeyboardButton(
        text="Вернуться в профиль",
        callback_data="profile"
    ))
    return keyboard.as_markup()


def return_keyboard(text, callback):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=f"{text}", callback_data=callback))
    return keyboard.as_markup()
