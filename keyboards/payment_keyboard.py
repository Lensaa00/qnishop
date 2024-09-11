from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def payment_keyboard(amount):
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width=1
    keyboard.add(
        InlineKeyboardButton(
            text=f"Оплатить {amount}₽",
            callback_data=f"payment_agree_{amount}"
        ),
        InlineKeyboardButton(
            text="Отмена платежа",
            callback_data="payment_cancel"
        )
    )
    return keyboard.as_markup()