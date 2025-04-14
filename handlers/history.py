from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("history"))
async def history_cmd(message: Message):
    await message.answer("История пока пуста 📜")
