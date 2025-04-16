# fitness-bot/keyboards/__init__.py
"""
Экспорт клавиатур для всего проекта.
"""

from .main import main_menu_kb, cancel_kb
from .plan import (
    view_plan_kb,
    edit_plan_options_kb,
    confirm_edit_kb
)
from .history import (
    history_kb,
    details_kb
)

__all__ = [
    'main_menu_kb',
    'cancel_kb',
    'view_plan_kb',
    'edit_plan_options_kb',
    'confirm_edit_kb',
    'history_kb',
    'details_kb'
]