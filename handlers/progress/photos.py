from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database import (
    get_progress_photos,
    add_progress_photo
)
from keyboards.progress import photos_kb
from utils import validate_photo

router = Router()

@router.message(Command("progress_photos"))
async def show_progress_photos(message: Message):
    photos = await get_progress_photos(message.from_user.id)
    
    if not photos:
        return await message.answer("У вас нет сохраненных фото прогресса")
    
    await message.answer_photo(
        photos[0]['file_id'],
        caption=f"Фото прогресса от {photos[0]['date']} (1/{len(photos)})",
        reply_markup=photos_kb(0, len(photos))
    )

@router.callback_query(F.data.startswith("photo_"))
async def navigate_photos(callback: CallbackQuery):
    action, index = callback.data.split("_")[1:]
    index = int(index)
    photos = await get_progress_photos(callback.from_user.id)
    
    if action == "next":
        new_index = (index + 1) % len(photos)
    else:
        new_index = (index - 1) % len(photos)
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=photos[new_index]['file_id'],
            caption=f"Фото прогресса от {photos[new_index]['date']} "
                   f"({new_index+1}/{len(photos)})"
        ),
        reply_markup=photos_kb(new_index, len(photos))
    )
    await callback.answer()

@router.message(F.photo)
async def save_progress_photo(message: Message):
    if not await validate_photo(message):
        return await message.answer(
            "Пожалуйста, отправляйте только фото прогресса"
        )
    
    photo_id = message.photo[-1].file_id
    success = await add_progress_photo(
        user_id=message.from_user.id,
        file_id=photo_id
    )
    
    if success:
        await message.answer("✅ Фото прогресса сохранено")
    else:
        await message.answer("❌ Ошибка при сохранении фото")