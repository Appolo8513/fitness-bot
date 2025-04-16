from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from database import get_workout_details
from keyboards.history import details_kb
from utils import format_workout_details

router = Router()

@router.callback_query(F.data.startswith("detail_"))
async def workout_details_handler(callback: CallbackQuery):
    workout_id = int(callback.data.split("_")[1])
    
    try:
        details = await get_workout_details(
            user_id=callback.from_user.id,
            workout_id=workout_id
        )
        
        if not details:
            raise ValueError("Тренировка не найдена")
            
        text = format_workout_details(details)
        
        await callback.message.edit_text(
            text,
            reply_markup=details_kb(workout_id)
        )
    except Exception as e:
        error_msg = f"Ошибка загрузки данных: {str(e)}"
        await callback.answer(error_msg, show_alert=True)