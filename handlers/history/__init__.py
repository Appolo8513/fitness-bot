# fitness-bot/handlers/history/__init__.py
"""
Роутер для работы с историей тренировок.
"""

from aiogram import Router
from .list import list_router
from .details import details_router

history_router = Router()
history_router.include_router(list_router)
history_router.include_router(details_router)

__all__ = ['history_router']