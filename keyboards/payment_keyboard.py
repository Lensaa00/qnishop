from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def payment_keyboard(amount):
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width=1
    keyboard.add(
        InlineKeyboardButton(
            text=f"Оплатить",
            callback_data=f"payment_agree_{amount}"
        ),
        InlineKeyboardButton(
            text="Отмена платежа",
            callback_data="start_callback"
        )
    )
    return keyboard.as_markup()

def successful_payment_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width=1
    keyboard.add(
        InlineKeyboardButton(
            text=f"Вернуться в меню",
            callback_data=f"start_callback"
        )
    )
    return keyboard.as_markup()