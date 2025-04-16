from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from database import get_current_plan, update_plan
from keyboards.plan import (
    edit_plan_kb,
    edit_plan_options_kb,
    confirm_edit_kb
)

router = Router()

class EditPlanStates(StatesGroup):
    select_option = State()
    edit_value = State()
    confirmation = State()

@router.callback_query(F.data == "edit_plan")
async def start_edit_plan(callback: CallbackQuery, state: FSMContext):
    plan = await get_current_plan(callback.from_user.id)
    if not plan:
        return await callback.answer(
            "У вас нет активного плана",
            show_alert=True
        )
    
    await state.update_data(original_plan=plan)
    await callback.message.edit_text(
        "Выберите параметр для изменения:",
        reply_markup=edit_plan_options_kb(plan)
    )
    await state.set_state(EditPlanStates.select_option)

@router.callback_query(
    EditPlanStates.select_option,
    F.data.startswith("edit_")
)
async def select_edit_option(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split("_")[1]
    await state.update_data(editing_field=field)
    
    data = await state.get_data()
    current_value = data['original_plan'].get(field, "")
    
    await callback.message.edit_text(
        f"Текущее значение: {current_value}\n"
        f"Введите новое значение для '{field}':",
        reply_markup=edit_plan_kb()
    )
    await state.set_state(EditPlanStates.edit_value)

@router.message(EditPlanStates.edit_value)
async def process_new_value(message: Message, state: FSMContext):
    new_value = message.text
    data = await state.get_data()
    field = data['editing_field']
    
    await state.update_data(new_value=new_value)
    
    await message.answer(
        f"Подтвердите изменение:\n\n"
        f"Параметр: {field}\n"
        f"Новое значение: {new_value}",
        reply_markup=confirm_edit_kb()
    )
    await state.set_state(EditPlanStates.confirmation)

@router.callback_query(
    EditPlanStates.confirmation,
    F.data == "confirm_edit"
)
async def confirm_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    field = data['editing_field']
    new_value = data['new_value']
    
    success = await update_plan(
        user_id=user_id,
        field=field,
        value=new_value
    )
    
    if success:
        response = "✅ План успешно обновлен"
    else:
        response = "❌ Ошибка при обновлении плана"
    
    await callback.message.edit_text(response)
    await state.clear()