from typing import List, Dict, Optional
import sqlite3
from datetime import datetime
import json

DATABASE_NAME = "fitness_bot.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        
        # Таблица пользователей
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            registration_date TEXT
        )
        """)
        
        # Таблица планов тренировок
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_plans (
            plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plan_type TEXT,
            frequency TEXT,
            exercises TEXT,  # JSON список упражнений
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)
        
        # Таблица истории тренировок
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_history (
            workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            duration INTEGER,
            exercises TEXT,  # JSON список упражнений
            calories INTEGER,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)
        
        # Таблица прогресса
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            weight REAL,
            body_fat REAL,
            photos TEXT,  # JSON список file_id
            measurements TEXT,  # JSON замеров тела
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)
        
        self.conn.commit()

    # Методы для работы с планами тренировок
    async def get_current_plan(self, user_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM training_plans 
        WHERE user_id = ? 
        ORDER BY updated_at DESC 
        LIMIT 1
        """, (user_id,))
        plan = cursor.fetchone()
        
        if plan:
            return {
                "plan_id": plan[0],
                "user_id": plan[1],
                "plan_type": plan[2],
                "frequency": plan[3],
                "exercises": json.loads(plan[4]),
                "created_at": plan[5],
                "updated_at": plan[6]
            }
        return None

    async def update_plan(self, user_id: int, field: str, value: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"""
            UPDATE training_plans 
            SET {field} = ?, updated_at = ?
            WHERE user_id = ? AND plan_id = (
                SELECT plan_id FROM training_plans 
                WHERE user_id = ? 
                ORDER BY updated_at DESC 
                LIMIT 1
            )
            """, (value, datetime.now().isoformat(), user_id, user_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    # Методы для истории тренировок
    async def get_workout_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM workout_history 
        WHERE user_id = ? 
        ORDER BY date DESC 
        LIMIT ?
        """, (user_id, limit))
        
        return [{
            "workout_id": row[0],
            "user_id": row[1],
            "date": row[2],
            "duration": row[3],
            "exercises": json.loads(row[4]),
            "calories": row[5],
            "notes": row[6]
        } for row in cursor.fetchall()]

    # Методы для прогресса
    async def get_user_stats(self, user_id: int, period: str = "month") -> Dict:
        cursor = self.conn.cursor()
        
        if period == "week":
            interval = "7 days"
        elif period == "month":
            interval = "30 days"
        else:  # all time
            interval = "100 years"
            
        cursor.execute(f"""
        SELECT 
            COUNT(*) as workouts_count,
            SUM(duration) as total_duration,
            AVG(calories) as avg_calories
        FROM workout_history
        WHERE user_id = ? AND date >= date('now', '-{interval}')
        """, (user_id,))
        
        stats = cursor.fetchone()
        return {
            "workouts": stats[0],
            "total_duration": stats[1],
            "avg_calories": stats[2]
        }

# Синглтон для доступа к БД
db = Database()