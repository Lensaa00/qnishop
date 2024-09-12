from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.admin_handlers import database

router = Router()

@router.callback_query(F.data.contains("category_open_"))
async def category_open(callback: CallbackQuery):
    query = callback.data.split("_")
    category = database.get_categories()
    items = database.get_items_by_category(query[2])
    await callback.message.edit_text(
        text=f"Категория {query[1]}"
    )