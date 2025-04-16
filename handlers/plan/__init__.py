# fitness-bot/handlers/plan/__init__.py
"""
Роутер для управления планами тренировок.
"""

from aiogram import Router
from .create_plan import create_router
from .edit_plan import edit_router
from .view_plan import view_router

plan_router = Router()
plan_router.include_router(create_router)
plan_router.include_router(edit_router)
plan_router.include_router(view_router)

__all__ = ['plan_router']