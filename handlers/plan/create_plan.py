from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from states import CreatePlanStates

router = Router()

@router.callback_query(F.data == "create_plan")
async def start_creating_plan(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Выберите тип тренировок:\n"
        "1) Силовые\n2) Кардио\n3) Смешанные"
    )
    await state.set_state(CreatePlanStates.choosing_type)