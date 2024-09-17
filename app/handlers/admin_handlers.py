from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.sql.functions import user

from app.database import requests as rq
from app.keyboards import admin_keyboards as admin_kb
from app.keyboards import menu_keyboards as menu_kb

router = Router()


@router.message(Command("admin"))
async def admin(message: Message):
    await message.delete()
    user = await rq.get_user(message.from_user.id)
    if user.is_admin:
        await message.answer(
            text="Панель администратора",
            reply_markup=admin_kb.admin_keyboard()
        )


@router.callback_query(F.data == "admin")
async def admin_callback(callback: CallbackQuery):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await callback.message.edit_text(
            text="Панель администратора",
            reply_markup=admin_kb.admin_keyboard(),
            parse_mode=ParseMode.MARKDOWN_V2
        )


@router.callback_query(F.data == "admin_manage_rights")
async def admin_manage_rights_callback(callback: CallbackQuery):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await callback.message.edit_text(
            text="Панель администратора\nНастройка прав пользователей",
            reply_markup=admin_kb.admin_rights_keyboard(),
            parse_mode=ParseMode.MARKDOWN_V2
        )


@router.callback_query(F.data == "admin_manage_rights_admin_list")
async def admin_list_callback(callback: CallbackQuery):
    users = await rq.get_users()
    callback_user = await rq.get_user(callback.from_user.id)
    admins_counter = 0
    message_text = f"Список администраторов\n"
    if callback_user.is_admin:
        for user in users:
            if user.is_admin:
                admins_counter += 1
                message_text += f"{admins_counter}. <code>{user.telegram_username}</code> <code>{user.telegram_id}</code>\n"
                message_text += "\n"

        message_text += f"Всего администраторов: {admins_counter}"
        await callback.message.edit_text(
            text=message_text,
            reply_markup=menu_kb.return_keyboard("Вернуться в админ-панель", "admin"),
            parse_mode=ParseMode.HTML
        )


@router.callback_query(F.data == "admin_manage_items")
async def admin_manage_items_callback(callback: CallbackQuery):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await callback.message.edit_text(
            text="Панель администратора\nНастройка товара",
            reply_markup=admin_kb.admin_items_keyboard(),
            parse_mode=ParseMode.MARKDOWN_V2
        )


@router.callback_query(F.data == "admin_close")
async def admin_close_callback(callback: CallbackQuery):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await callback.message.delete()
