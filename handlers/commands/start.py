from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.main import menu_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🏋️ Добро пожаловать в FitnessBot!\n\n"
        "Я помогу вам с тренировками, питанием и отслеживанием прогресса.",
        reply_markup=menu_keyboard()
    )