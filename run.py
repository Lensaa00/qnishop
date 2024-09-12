import asyncio
from aiogram import Bot, Dispatcher

from handlers import main_handlers, payment_handlers, admin_handlers, category_handlers
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(
        main_handlers.router,
        payment_handlers.router,
        admin_handlers.router,
        category_handlers.router
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
