from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    InlineKeyboardButton
)

def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Мой план")
    builder.button(text="📈 Прогресс")
    builder.button(text="📅 История")
    builder.button(text="⚙️ Настройки")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)