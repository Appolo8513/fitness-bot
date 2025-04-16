# fitness-bot/models/__init__.py
"""
Экспорт моделей данных.
"""

from .user import User
from .plan import TrainingPlan
from .progress import ProgressRecord

__all__ = ['User', 'TrainingPlan', 'ProgressRecord']