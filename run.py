import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import menu_handlers, advert_handlers, admin_handlers
from app.database.models import async_main
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await async_main()
    dp.include_routers(
        menu_handlers.router,
        admin_handlers.router,
        advert_handlers.router,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
