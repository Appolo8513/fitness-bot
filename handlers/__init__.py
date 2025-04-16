# fitness-bot/handlers/__init__.py
"""
Агрегатор всех хендлеров бота.
Собирает роутеры из подпакетов в главный роутер.
"""

from aiogram import Router
from .commands import commands_router
from .history import history_router
from .plan import plan_router
from .progress import progress_router
from .errors import errors_router

main_router = Router()
main_router.include_routers(
    commands_router,
    history_router,
    plan_router,
    progress_router,
    errors_router
)

__all__ = ['main_router']