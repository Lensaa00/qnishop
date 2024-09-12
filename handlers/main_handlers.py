from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject
from aiogram.enums import ParseMode
from aiogram.utils.deep_linking import decode_payload, create_start_link

import config
from keyboards import main_keyboards as main_kb
from database import Database

database = Database("database.db")
router = Router()
bot = Bot(config.TOKEN)


@router.message(CommandStart())
async def start(message: Message, command: CommandObject = None):
    if not database.user_exists(message.from_user.id):
        if command:
            args = command.args
            if not args is None:
                payload = decode_payload(args)
                database.create_user_referral(message.from_user.id, message.from_user.username, payload)
                await bot.send_message(
                    chat_id=payload,
                    text="Пользователь зарегистрировался по вашей ссылке."
                )
            else:
                database.create_user(message.from_user.id, message.from_user.username)
        else:
            database.create_user(message.from_user.id, message.from_user.username)

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
    categories = database.get_categories()
    await callback.message.edit_text(
        text="<b>Каталог</b>\nВыберите пункт меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=main_kb.catalog_keyboard(categories)
    )


@router.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    user = database.get_user(callback.from_user.id)
    referrals = database.get_user_referrals(callback.from_user.id)
    await callback.message.edit_text(
        text=f"Профиль *{callback.from_user.username.upper()}*\nВаш ID: *`{user[1]}`*\nВаши рефералы: *{referrals}*\nВаш баланс: *{user[4]} руб*",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=main_kb.profile_keyboard()
    )


@router.callback_query(F.data == "get_referral_link")
async def get_referral_link(callback: CallbackQuery):
    link = await create_start_link(bot, str(callback.from_user.id), encode=True)
    await callback.message.edit_text(
        text=f"Ваша реферальная ссылка\n`{link}`",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=main_kb.referral_keyboard()
    )
