from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def items_keyboard(items):
    keyboard = InlineKeyboardBuilder()
    for item in items:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{item[1]} | {item[2]}руб.",
                callback_data=f"buy_item_id_{item[0]}"
            )
        )