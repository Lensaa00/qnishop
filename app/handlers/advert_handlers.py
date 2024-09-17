from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, Update
from app.database import requests as rq
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from config import TOKEN
from app.keyboards import advert_keyboards as ad_kb

router = Router()
bot = Bot(token=TOKEN)


class Advert(StatesGroup):
    image = State()
    text = State()
    url = State()


async def send_advert(update: Update, data: dict):
    if isinstance(update, CallbackQuery):
        user_id = update.from_user.id
        message = update.message
    elif isinstance(update, Message):
        user_id = update.from_user.id
        message = update
    else:
        raise ValueError("Invalid update type")

    if not data.get("image") and not data.get("text") and not data.get("url"):
        await message.edit_text("Рассылка отменена, так как все шаги были пропущены.")
    else:
        # Рассылка пользователям
        users = await rq.get_users()
        print(data)
        for user in users:
            # Проверка, есть ли картинка, текст и ссылка
            if data.get("image") and data.get("text") and data.get("url"):
                await bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=data.get("image"),
                    caption=data.get("text"),
                    parse_mode=ParseMode.HTML,
                    reply_markup=ad_kb.advert_link(data.get("url"))
                )
            # Проверка, есть ли картинка и текст (без ссылки)
            elif data.get("image") and data.get("text"):
                await bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=data.get("image"),
                    caption=data.get("text"),
                    parse_mode=ParseMode.HTML
                )
            # Проверка, есть ли текст и ссылка (без картинки)
            elif data.get("text") and data.get("url"):
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=data.get("text"),
                    parse_mode=ParseMode.HTML,
                    reply_markup=ad_kb.advert_link(data.get("url"))
                )
            # Проверка, есть ли только текст
            elif data.get("text"):
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=data.get("text"),
                    parse_mode=ParseMode.HTML
                )
            # Проверка, есть ли только картинка
            elif data.get("image"):
                await bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=data.get("image")
                )
            # Если нет ни текста, ни картинки
            else:
                await message.answer(
                    text="Ошибка в отправке рассылки\nПроверьте вводимые данные и попробуйте снова."
                )
                return


@router.callback_query(F.data == "admin_advertise")
async def admin_advertise_callback(callback: CallbackQuery, state: FSMContext):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await state.set_state(Advert.image)
        await callback.message.edit_text(
            text="Отправьте картинку для рассылки:",
            reply_markup=ad_kb.skip_step_image(),
        )


@router.message(Advert.image)
async def advert_image_step(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if user.is_admin:
        if message.photo:
            photo_id = message.photo[-1].file_id
            await state.update_data(image=photo_id)
        else:
            await message.answer("Пожалуйста, отправьте изображение.")
            return
        await state.set_state(Advert.text)
        await message.answer(
            text="Отправьте текст рассылки:",
            reply_markup=ad_kb.skip_step_text(),
        )


@router.message(Advert.text)
async def advert_text_step(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if user.is_admin:
        if message.text:
            # await state.update_data(text=message.text.replace("!", "").replace(".", ""))
            await state.update_data(text=message.text)
        else:
            await message.answer("Пожалуйста, отправьте текст.")
            return
        await state.set_state(Advert.url)
        await message.answer(
            text="Отправьте ссылку для кнопки рассылки:",
            reply_markup=ad_kb.skip_step_url(),
        )


@router.message(Advert.url)
async def advert_url_step(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if user.is_admin:
        await state.update_data(url=message.text)
        data = await state.get_data()
        await send_advert(message, data)
        await state.clear()


@router.callback_query(F.data == "skip_step_image")
async def skip_step_image_callback(callback: CallbackQuery, state: FSMContext):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await state.update_data(image=None)
        await state.set_state(Advert.text)
        await callback.message.edit_text(
            text="Отправьте текст рассылки:",
            reply_markup=ad_kb.skip_step_text(),
        )


@router.callback_query(F.data == "skip_step_text")
async def skip_step_text_callback(callback: CallbackQuery, state: FSMContext):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await state.update_data(text=None)
        await state.set_state(Advert.url)
        await callback.message.edit_text(
            text="Отправьте ссылку для кнопки рассылки:",
            reply_markup=ad_kb.skip_step_url(),
        )


@router.callback_query(F.data == "skip_step_url")
async def skip_step_url_callback(callback: CallbackQuery, state: FSMContext):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await state.update_data(url=None)
        data = await state.get_data()

        await send_advert(callback, data)
        await state.clear()
