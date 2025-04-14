from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привет! Я твой фитнес-тренер 🏋️\n\nИспользуй:\n/start — приветствие\n/plan — твой план\n/progress — прогресс\n/history — история тренировок")
