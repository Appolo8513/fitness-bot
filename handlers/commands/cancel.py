from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

router = Router()

@router.message(Command("cancel"))
@router.callback_query(F.data == "cancel")
async def cancel_handler(
    update: Message | CallbackQuery, 
    state: FSMContext
):
    current_state = await state.get_state()
    if not current_state:
        response = "Нет активных действий для отмены"
    else:
        await state.clear()
        response = "❌ Действие отменено"

    try:
        if isinstance(update, Message):
            await update.answer(response)
        else:
            await update.message.edit_text(
                response,
                reply_markup=None
            )
            await update.answer()
    except TelegramBadRequest:
        pass  # Уже было изменено сообщение