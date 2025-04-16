from database import async_db_session

async def on_startup():
    await async_db_session.init()
    await async_db_session.create_all()

async def on_shutdown():
    await async_db_session.close()

# Изменить блок start_polling:
await dp.start_polling(
    bot,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    allowed_updates=dp.resolve_used_update_types()
)

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Импортируем главный роутер из handlers
from handlers import main_router

# Импортируем утилиты и настройки
from utils import setup_logging
from config import load_config

# Настройка логирования
logger = logging.getLogger(__name__)

async def main():
    # 1. Загрузка конфигурации
    config = load_config()
    
    # 2. Инициализация хранилища FSM
    storage = MemoryStorage()  # Для продакшена лучше использовать RedisStorage
    
    # 3. Создание экземпляров бота и диспетчера
    bot = Bot(
        token=config.bot.token,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
    dp = Dispatcher(storage=storage)
    
    # 4. Подключение роутеров
    dp.include_router(main_router)
    
    # 5. Пользовательские middleware (пример)
    # dp.update.middleware(SomeMiddleware())
    
    # 6. Запуск поллинга
    logger.info("Бот запущен")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            polling_timeout=30
        )
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    # Настройка логирования
    setup_logging()
    
    try:
        # Запуск асинхронного event loop
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен вручную")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}", exc_info=True)