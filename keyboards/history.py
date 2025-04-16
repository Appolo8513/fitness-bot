from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def history_kb(workouts: list, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for workout in workouts:
        builder.button(
            text=f"{workout['date']} - {workout['duration']} мин",
            callback_data=f"detail_{workout['workout_id']}"
        )
    
    # Навигация
    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=f"history_page_{page-1}")
    builder.button(text=f"{page}", callback_data="current_page")
    builder.button(text="Вперед ➡️", callback_data=f"history_page_{page+1}")
    
    builder.adjust(1, 3)
    return builder.as_markup()