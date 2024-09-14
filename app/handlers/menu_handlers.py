from ast import parse
from types import NoneType

from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload

import config
from app.database import requests as rq
from app.keyboards import menu_keyboards as menu_kb

router = Router()
bot = Bot(config.TOKEN)


@router.message(CommandStart())
async def start_command(message: Message, command: CommandObject = None):
    telegram_id = message.from_user.id
    telegram_username = message.from_user.username

    if command and command.args:
        args = command.args
        payload = decode_payload(args)
        await rq.add_user_referral(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            telegram_referral_id=payload
        )
    else:
        await rq.add_user(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
        )

    await message.answer(
        text="Добро пожаловать в QniShop",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_kb.start()
    )


@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Добро пожаловать в QniShop",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_kb.start()
    )


@router.callback_query(F.data == "catalog")
async def catalog_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text="*Каталог*\nВыберите категорию:",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=await menu_kb.catalog()
    )


@router.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    user = await rq.get_user(telegram_id=callback.from_user.id)
    await callback.message.edit_text(
        text=f"Профиль *{user.telegram_username}*\nБаланс: {user.balance} руб ",
        reply_markup=menu_kb.profile(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data == "balance")
async def balance_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text="*Пополнение баланса*\nВыберите сумму для пополнения:",
        reply_markup=menu_kb.deposit_keyboard(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("category_"))
async def category_callback(callback: CallbackQuery):
    query = callback.data.split("_")
    category = await rq.get_category_by_id(query[1])
    await callback.message.edit_text(
        text=f"Категория *{category.name}*\nВыберите товар:",
        reply_markup=await menu_kb.items(category.id),
        parse_mode=ParseMode.MARKDOWN_V2
    )


@router.callback_query(F.data.startswith("deposit_"))
async def deposit_callback(callback: CallbackQuery):
    query = callback.data.split("_")
    amount = int(query[1])

    await callback.message.delete()
    price = LabeledPrice(label="Пополнение баланса", amount=amount * 100)
    await bot.send_invoice(
        callback.message.chat.id,
        title="Оплата товара",
        description="Пополнение баланса QniShop",
        provider_token=config.PAYMASTER,
        currency='rub',
        is_flexible=False,
        prices=[price],
        payload='item_pay'
    )


@router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await rq.balance_deposit(message.from_user.id, round(message.successful_payment.total_amount / 100))
    await message.answer(
        text=f"Оплата успешно прошла.\nВаш баланс пополнен на {round(message.successful_payment.total_amount / 100)}руб.",
        reply_markup=menu_kb.return_keyboard("Вернуться в меню", "start")
    )


@router.callback_query(F.data == "get_referral")
async def get_referral_callback(callback: CallbackQuery):
    link = await create_start_link(bot, str(callback.from_user.id), encode=True)
    await callback.message.edit_text(
        text=f"*Ваша реферальная ссылка QniShop*\n`{link}`",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=menu_kb.return_keyboard("Вернуться в меню", "start")
    )
