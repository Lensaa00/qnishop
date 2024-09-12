from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def admin_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width=1
    keyboard.add(
        InlineKeyboardButton(
            text=f"Добавить администратора",
            callback_data=f"admin_add_user"
        ),
        InlineKeyboardButton(
            text=f"Вернуться в меню",
            callback_data=f"start_callback"
        )
    )
    return keyboard.as_markup()