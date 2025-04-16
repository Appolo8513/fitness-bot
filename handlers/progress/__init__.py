# fitness-bot/handlers/progress/__init__.py
"""
Роутер для отслеживания прогресса.
"""

from aiogram import Router
from .photos import photos_router
from .stats import stats_router

progress_router = Router()
progress_router.include_router(photos_router)
progress_router.include_router(stats_router)

__all__ = ['progress_router']