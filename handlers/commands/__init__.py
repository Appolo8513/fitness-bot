# fitness-bot/handlers/commands/__init__.py
"""
Роутер команд (старт, помощь, отмена).
"""

from aiogram import Router
from .start import start_router
from .cancel import cancel_router

commands_router = Router()
commands_router.include_router(start_router)
commands_router.include_router(cancel_router)

__all__ = ['commands_router']