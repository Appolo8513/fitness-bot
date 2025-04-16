from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import get_workout_history
from keyboards.history import history_kb
from utils import paginate_history

router = Router()

@router.message(Command("history"))
async def history_command(message: Message):
    workouts = await get_workout_history(message.from_user.id)
    if not workouts:
        return await message.answer("История тренировок пуста")
    
    page = 1
    paged_data = paginate_history(workouts, page)
    
    await message.answer(
        f"📅 История тренировок (страница {page}):",
        reply_markup=history_kb(paged_data, page)
    )

@router.callback_query(F.data.startswith("history_page_"))
async def history_page_handler(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    workouts = await get_workout_history(callback.from_user.id)
    
    paged_data = paginate_history(workouts, page)
    
    await callback.message.edit_text(
        f"📅 История тренировок (страница {page}):",
        reply_markup=history_kb(paged_data, page)
    )
    await callback.answer()