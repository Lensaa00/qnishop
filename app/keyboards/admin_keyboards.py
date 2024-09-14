from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Главная клавиатура админ-панели
def admin_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 1
    keyboard.add(
        InlineKeyboardButton(
            text="Права",
            callback_data="admin_manage_rights"
        ),
        InlineKeyboardButton(
            text="Товары",
            callback_data="admin_manage_items"
        ),
        InlineKeyboardButton(
            text="Рассылка",
            callback_data="admin_manage_keyboard"
        ),
        InlineKeyboardButton(
            text="Закрыть меню",
            callback_data="admin_close"
        )
    )
    return keyboard.as_markup()


# Клавиатура настройки прав пользователей
def admin_rights_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 1
    keyboard.add(
        InlineKeyboardButton(
            text="Список администраторов",
            callback_data="admin_rights_list"
        ),
        InlineKeyboardButton(
            text="Добавить администратора",
            callback_data="admin_rights_add_admin"
        ),
        InlineKeyboardButton(
            text="Удалить администратора",
            callback_data="admin_rights_remove_admin"
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data="admin"
        )
    )
    return keyboard.as_markup()


# Клавиатура настройки товаров
def admin_items_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 1
    keyboard.add(
        InlineKeyboardButton(
            text="Список товаров",
            callback_data="admin_items_get_all"
        ),
        InlineKeyboardButton(
            text="Добавить товар",
            callback_data="admin_items_add"
        ),
        InlineKeyboardButton(
            text="Удалить товар",
            callback_data="admin_items_remove"
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data="admin"
        )
    )
    return keyboard.as_markup()
