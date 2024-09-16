from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def skip_step_image():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Пропустить",
            callback_data=f"skip_step_image"
        )
    )
    return keyboard.as_markup()


def skip_step_text():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Пропустить",
            callback_data=f"skip_step_text"
        )
    )
    return keyboard.as_markup()


def skip_step_url():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Пропустить",
            callback_data=f"skip_step_url"
        )
    )
    return keyboard.as_markup()


def advert_link(url):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Открыть ссылку",
            url=url
        )
    )
    return keyboard.as_markup()
