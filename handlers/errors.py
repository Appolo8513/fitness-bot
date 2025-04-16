from aiogram import Router
from aiogram.types import ErrorEvent
from aiogram import Bot

router = Router()

@router.error()
async def error_handler(event: ErrorEvent, bot: Bot):
    await bot.send_message(
        event.update.message.from_user.id,
        "⚠️ Произошла ошибка. Пожалуйста, попробуйте позже."
    )
    # Логирование ошибки
    print(f"Ошибка: {event.exception}")