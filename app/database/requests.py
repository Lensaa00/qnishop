from app.database.models import async_session
from app.database.models import User, Category, Item
from sqlalchemy import select, update, delete


# ПОЛЬЗОВАТЕЛИ
# добавление пользователя без реферала
async def add_user(telegram_id, telegram_username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        if not user:
            session.add(User(
                telegram_id=telegram_id,
                telegram_username=telegram_username
            ))
            await session.commit()


# добавление пользователя с рефералом
async def add_user_referral(telegram_id, telegram_username, telegram_referral_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        if not user:
            session.add(User(
                telegram_id=telegram_id,
                telegram_username=telegram_username,
                telegram_referral_id=telegram_referral_id,
            ))
            await session.commit()


# получения объекта пользователя
async def get_user(telegram_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.telegram_id == telegram_id))

async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User).order_by(User.telegram_id))


# КАТЕГОРИИ
# получить все категории
async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


# получить категорию по id
async def get_category_by_id(category_id):
    async with async_session() as session:
        return await session.scalar(select(Category).where(Category.id == category_id))


# ТОВАРЫ
# получить товары в категории
async def get_items_by_category_id(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


# получить товар по айди
async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))


# БАЛАНС
# пополнение баланса пользователя
async def balance_deposit(telegram_id, amount):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        balance = user.balance + amount
        await session.execute(update(User).where(User.telegram_id == telegram_id).values(balance=balance))
        await session.commit()
