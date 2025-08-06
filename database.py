import asyncpg
import logging
from config import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        """Создание пула соединений с базой данных"""
        try:
            self.pool = await asyncpg.create_pool(DATABASE_URL)
            logger.info("Соединение с базой данных установлено")
            await self.create_tables()
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise
    
    async def disconnect(self):
        """Закрытие пула соединений"""
        if self.pool:
            await self.pool.close()
            logger.info("Соединение с базой данных закрыто")
    
    async def create_tables(self):
        """Создание таблицы пользователей"""
        async with self.pool.acquire() as connection:
            await connection.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT UNIQUE NOT NULL,
                    username VARCHAR(255),
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            logger.info("Таблица users создана или уже существует")
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Добавление или обновление пользователя"""
        async with self.pool.acquire() as connection:
            await connection.execute('''
                INSERT INTO users (user_id, username, first_name, last_name, updated_at)
                VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id) 
                DO UPDATE SET 
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    updated_at = CURRENT_TIMESTAMP
            ''', user_id, username, first_name, last_name)
            logger.info(f"Пользователь {user_id} добавлен/обновлен в базе данных")
    
    async def get_user(self, user_id: int):
        """Получение информации о пользователе"""
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(
                'SELECT * FROM users WHERE user_id = $1', user_id
            )
            return dict(result) if result else None
    
    async def get_all_users(self):
        """Получение всех пользователей"""
        async with self.pool.acquire() as connection:
            results = await connection.fetch('SELECT * FROM users ORDER BY created_at')
            return [dict(row) for row in results]

# Создаем глобальный экземпляр базы данных
db = Database() 