from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.sql.functions import user

import config
from app.database import requests as rq
from app.keyboards import admin_keyboards as admin_kb
from app.keyboards import menu_keyboards as menu_kb

router = Router()
bot = Bot(token=config.TOKEN)


class AdminAdd(StatesGroup):
    telegram_id = State()


class AdminRemove(StatesGroup):
    telegram_id = State()


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


@router.callback_query(F.data == "admin_manage_rights_admin_add")
async def admin_manage_rights_add_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminAdd.telegram_id)
    await callback.message.edit_text(
        text="Добавление администратора\nОтправьте ID пользователя, для выдачи прав администратора:"
    )


@router.message(AdminAdd.telegram_id)
async def admin_manage_rights_add_step_1(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(telegram_id=message.text)
        data = await state.get_data()
        user = await rq.get_user(data.get("telegram_id"))
        if user and not user.is_admin:
            await state.clear()
            await rq.user_add_admin(telegram_id=data.get("telegram_id"))
            await bot.send_message(
                chat_id=data.get("telegram_id"),
                text="Вы были добавлены в администраторы бота.\nДля получения доступа к меню администратора, отправьте в чат команду /admin"
            )
            await message.answer(
                text=f"Пользователь {user.telegram_username} добавлен в администраторы."
            )
        else:
            await message.answer(
                text="Пользователь уже является администратором, или его нет в базе данных бота. Проверьте вводимые данные."
            )
            return


@router.callback_query(F.data == "admin_manage_rights_admin_remove")
async def admin_manage_rights_remove_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminRemove.telegram_id)
    await callback.message.edit_text(
        text="Удаление администратора\nОтправьте ID пользователя, для удаления прав администратора:"
    )


@router.message(AdminRemove.telegram_id)
async def admin_manage_rights_remove_step_1(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(telegram_id=message.text)
        data = await state.get_data()
        user = await rq.get_user(data.get("telegram_id"))
        if user and user.is_admin and message.from_user.id != data.get("telegram_id"):
            if not data.get("telegram_id") == config.MAIN_ADMIN_ID:
                await state.clear()
                await rq.user_remove_admin(telegram_id=data.get("telegram_id"))
                await bot.send_message(
                    chat_id=data.get("telegram_id"),
                    text="Вы были удалены из администраторов бота."
                )
                await message.answer(
                    text=f"Пользователь {user.telegram_username} был удален из администраторов."
                )
            else:
                await message.answer(
                    text="Вы не можете удалить этого администратора. Проверьте вводимые данные."
                )
                return
        else:
            await message.answer(
                text="Пользователь не является администратором, или его нет в базе данных бота. Проверьте вводимые данные."
            )
            return


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
