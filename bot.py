import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio

from handlers.plan import get_training_plan

API_TOKEN = '7274015743:AAF00b-IIWIeIJd0JxQTHLm-5RVIjSexLa4'#не стоит прописывать токен в теле бота - небезопасно

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Память для хранения количества подтягиваний
user_data = {}
current_exercise = {}

# Клавиатуры
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="План 🗓")],
        [KeyboardButton(text="Прогресс 📈")],
        [KeyboardButton(text="История 🕘")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие"
)

plan_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать тренировку")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие"
)

start_training_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить количество повторений")],
        [KeyboardButton(text="Закончить упражнение")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие"
)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я твой фитнес-тренер 🏋️\nВыбери, что хочешь узнать:",
        reply_markup=main_menu_keyboard
    )

@router.message(lambda msg: msg.text == "План 🗓")
async def handle_plan(message: Message):
    await message.answer(get_training_plan(), parse_mode="Markdown", reply_markup=plan_keyboard)

@router.message(lambda msg: msg.text == "Прогресс 📈")
async def handle_progress(message: Message):
    user_id = message.from_user.id
    total = user_data.get(user_id, 0)
    await message.answer(f"📈 Ты всего подтянулся: *{total}* раз", parse_mode="Markdown")

@router.message(lambda msg: msg.text == "История 🕘")
async def handle_history(message: Message):
    await message.answer("История твоих тренировок...")

# Когда пользователь нажимает "Начать тренировку"
@router.message(lambda msg: msg.text == "Начать тренировку")
async def start_training(message: Message):
    await message.answer(
        "Отлично! Готов к тренировке? Когда сделаешь подход, нажми 'Добавить количество повторений'.",
        reply_markup=start_training_keyboard
    )
    # Начинаем упражнение
    user_id = message.from_user.id
    current_exercise[user_id] = {'name': 'Подтягивания', 'reps': 0}

# Когда нажимает "Добавить количество повторений"
@router.message(lambda msg: msg.text == "Добавить количество повторений")
async def cmd_add(message: Message):
    await message.answer("✍️ Введи, сколько раз ты подтянулся (например: 12):")

# Когда нажимает "Закончить упражнение"
@router.message(lambda msg: msg.text == "Закончить упражнение")
async def finish_exercise(message: Message):
    user_id = message.from_user.id
    exercise = current_exercise.get(user_id)

    if exercise:
        await message.answer(
            f"Ты завершил упражнение *{exercise['name']}* с результатом {exercise['reps']} повторений.",
            parse_mode="Markdown"
        )
        # Удалим текущее упражнение из памяти
        del current_exercise[user_id]
        await message.answer(
            "Ты можешь начать новое упражнение или вернуться в главное меню.",
            reply_markup=main_menu_keyboard
        )
    else:
        await message.answer("Ты не начал упражнение. Пожалуйста, начни тренировку.")

# Приём чисел после /add
@router.message(F.text.regexp(r"^\d+$"))
async def handle_pullups_input(message: Message):
    user_id = message.from_user.id
    count = int(message.text)

    if user_id not in user_data:
        user_data[user_id] = 0

    if user_id in current_exercise:
        current_exercise[user_id]['reps'] += count
        await message.answer(f"✅ Добавил {count} повторений в упражнение. Всего: {current_exercise[user_id]['reps']} повторений.")
    else:
        user_data[user_id] += count
        await message.answer(f"✅ Добавил {count} повторений. Всего: {user_data[user_id]} 💪")

# Запуск
async def main():
    dp.include_router(router)
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
