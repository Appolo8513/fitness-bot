from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database import get_user_stats

router = Router()

@router.message(Command("progress"))
async def show_progress(message: Message):
    stats = await get_user_stats(message.from_user.id)
    await message.answer(
        f"📊 Ваш прогресс:\n\n"
        f"• Тренировок выполнено: {stats['workouts']}\n"
        f"• Потеряно веса: {stats['weight_loss']} кг\n"
        f"• Набрано мышц: {stats['muscle_gain']} кг"
    )