from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from app.database import requests as rq

from app.keyboards import admin_keyboards as admin_kb

router = Router()


@router.message(Command("admin"))
async def admin(message: Message):
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


@router.callback_query(F.data == "admin_close")
async def admin_close_callback(callback: CallbackQuery):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await callback.message.delete()
