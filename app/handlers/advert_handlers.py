from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
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
            await state.update_data(text=message.text.replace("!", "").replace(".", ""))
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

        # Проверка на наличие хотя бы одного шага
        if not data.get("image") and not data.get("text") and not data.get("url"):
            await message.answer("Рассылка отменена, так как все шаги были пропущены.")
            await state.clear()
            return

        # Рассылка пользователям
        users = await rq.get_users()
        for user in users:
            if data.get("image") and data.get("text"):
                await bot.send_photo(
                    user.telegram_id,
                    data["image"],
                    caption=data["text"],
                    reply_markup=ad_kb.advert_link(data["url"])
                )
            elif data.get("text"):
                await bot.send_message(
                    user.telegram_id,
                    data["text"],
                    reply_markup=ad_kb.advert_link(data["url"])
                )
            elif data.get("image"):
                await bot.send_photo(
                    user.telegram_id,
                    data["image"]
                )
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

        # Проверка на наличие хотя бы одного шага перед отправкой
        if not data.get("image") and not data.get("text") and not data.get("url"):
            await callback.message.answer("Рассылка отменена, так как все шаги были пропущены.")
            await state.clear()
        else:
            # Рассылка пользователям
            users = await rq.get_users()
            for user in users:
                if data.get("image") and data.get("text"):
                    await bot.send_photo(
                        user.telegram_id,
                        data["image"],
                        caption=data["text"],
                        reply_markup=ad_kb.advert_link(data["url"])
                    )
                elif data.get("text"):
                    await bot.send_message(
                        user.telegram_id,
                        data["text"],
                        reply_markup=ad_kb.advert_link(data["url"])
                    )
                elif data.get("image"):
                    await bot.send_photo(
                        user.telegram_id,
                        data["image"]
                    )
            await state.clear()
