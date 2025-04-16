from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import get_current_plan
from keyboards.plan import plan_actions_kb

router = Router()

@router.message(Command("plan"))
@router.callback_query(F.data == "view_plan")
async def view_plan(update: Message | CallbackQuery):
    plan = await get_current_plan(update.from_user.id)
    
    text = (
        "📝 Ваш текущий план:\n\n"
        f"Тип: {plan['type']}\n"
        f"Частота: {plan['frequency']}\n"
        f"Упражнения: {plan['exercises']}"
    )
    
    if isinstance(update, Message):
        await update.answer(text, reply_markup=plan_actions_kb())
    else:
        await update.message.edit_text(text, reply_markup=plan_actions_kb())