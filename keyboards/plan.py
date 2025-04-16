from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def view_plan_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Редактировать", callback_data="edit_plan")
    builder.button(text="🔄 Обновить", callback_data="view_plan")
    builder.button(text="🗑️ Удалить", callback_data="delete_plan")
    builder.adjust(2)
    return builder.as_markup()

def edit_plan_options_kb(plan: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Тип ({plan['plan_type']})", 
        callback_data="edit_type"
    )
    builder.button(
        text=f"Частота ({plan['frequency']})", 
        callback_data="edit_frequency"
    )
    builder.button(
        text="Упражнения", 
        callback_data="edit_exercises"
    )
    builder.button(
        text="❌ Отмена", 
        callback_data="cancel"
    )
    builder.adjust(1)
    return builder.as_markup()