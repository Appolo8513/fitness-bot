from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
import asyncio
import logging

from config import BOT_TOKEN
from handlers import start, plan, progress, history

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Регистрируем хендлеры
    dp.include_routers(
        start.router,
        plan.router,
        progress.router,
        history.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
