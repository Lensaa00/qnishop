from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import config
from keyboards import admin_keyboards as admin_kb
from database import Database

database = Database("database.db")
router = Router()
bot = Bot(config.TOKEN)

class AdminUserAdd(StatesGroup):
    user_id = State()

@router.message(Command("admin"))
async def admin_callback(message: Message):
    if database.user_admin(message.from_user.id):
        await message.answer(
            text="<b>Админ панель</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=admin_kb.admin_keyboard()
        )

@router.callback_query(F.data=="admin_add_user")
async def admin_add_user_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminUserAdd.user_id)
    await callback.message.edit_text(
        text="Введите ID пользователя"
    )

@router.message(AdminUserAdd.user_id)
async def admin_add_user_step2(message: Message, state: FSMContext):
    user_id = message.text
    await state.update_data(user_id=user_id)
    data = await state.get_data()
    await state.clear()
    database.update_user_admin(message.from_user.id)
    await message.delete()
    await message.answer("Администратор успешно добавлен")