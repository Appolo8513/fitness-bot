from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("plan"))
async def plan_cmd(message: Message):
    await message.answer("План тренировок ещё не настроен 🛠️")
