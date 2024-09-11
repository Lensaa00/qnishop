from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode


from keyboards import main_keyboards as main_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text="Добро пожаловать в <b>QniShop!</b>\nВыберите необходимый пункт меню.",
        parse_mode=ParseMode.HTML,
        reply_markup=main_kb.start_keyboard()
    )


@router.callback_query(F.data == "start_callback")
async def start_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Добро пожаловать в <b>QniShop!</b>\nВыберите необходимый пункт меню.",
        parse_mode=ParseMode.HTML,
        reply_markup=main_kb.start_keyboard()
    )


@router.callback_query(F.data == "catalog")
async def catalog_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text="<b>Каталог</b>\nВыберите пункт меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=main_kb.catalog_keyboard()
    )


@router.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"Профиль <b>{callback.from_user.username.upper()}</b>\nВаш баланс: 0 руб.",
        parse_mode=ParseMode.HTML,
        reply_markup=main_kb.profile_keyboard()
    )



