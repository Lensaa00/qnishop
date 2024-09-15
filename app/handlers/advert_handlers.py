from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from app.database import requests as rq
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from config import TOKEN

from app.keyboards import advert_keyboards as ad_kb
from app.keyboards import admin_keyboards as admin_kb

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
            parse_mode=ParseMode.MARKDOWN_V2
        )

@router.message(Advert.image)
async def advert_image_step(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if user.is_admin:
        photo_id = message.photo[-1].file_id
        await state.update_data(image=photo_id)
        await state.set_state(Advert.text)
        await message.answer(
            text="Отправьте текст рассылки:",
            reply_markup=ad_kb.skip_step_text(),
            parse_mode=ParseMode.MARKDOWN_V2
        )

@router.message(Advert.text)
async def advert_text_step(message: Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)
    if user.is_admin:
        await state.update_data(text=message.text)
        await state.set_state(Advert.url)
        await message.answer(
            text="Отправьте ссылку для кнопки рассылки:",
            reply_markup=ad_kb.skip_step_url(),
            parse_mode=ParseMode.MARKDOWN_V2
        )

@router.callback_query(F.data == "skip_step_image")
async def skip_step_image_callback(callback: CallbackQuery, state: FSMContext):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await state.update_data(image=None)
        await state.set_state(Advert.text)
        await callback.message.edit_text(
            text="Отправьте текст рассылки:",
            reply_markup=ad_kb.skip_step_text(),
            parse_mode=ParseMode.MARKDOWN_V2
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
            parse_mode=ParseMode.MARKDOWN_V2
        )


@router.callback_query(F.data == "skip_step_url")
async def skip_step_url_callback(callback: CallbackQuery, state: FSMContext):
    user = await rq.get_user(callback.from_user.id)
    if user.is_admin:
        await state.update_data(url=None)
        await state.clear()
        data = await state.get_data()

        image = data["image"]
        text = data["text"]
        url = data["url"]

        users = await rq.get_users()

        if text is not None:
            if image is not None:
                if url is not None:
                    for user in users:
                        await bot.send_photo(
                            chat_id=user.id,
                            photo=image,
                            caption=text,
                            reply_markup=ad_kb.advert_link(url)
                        )
            elif url is not None:
                pass
            else:
                pass
        else:
            pass

        await callback.message.answer(
            text="Панель администратора",
            reply_markup=admin_kb.admin_keyboard()
        )
