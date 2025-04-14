from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("progress"))
async def progress_cmd(message: Message):
    await message.answer("Прогресс ещё не отслеживается 📉")
