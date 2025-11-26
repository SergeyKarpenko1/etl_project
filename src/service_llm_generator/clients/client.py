from typing import List, Dict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DBClient:
    """Асинхронный клиент для взаимодействия с PostgreSQL."""

    def __init__(self, dsn: str):
        """
        dsn: строка подключения, пример:
        postgresql+asyncpg://user:password@localhost:5432/dbname
        """
        self.dsn = dsn
        self._engine = create_async_engine(self.dsn, echo=False)
        self._async_session = sessionmaker(
            bind=self._engine, class_=AsyncSession, expire_on_commit=False
        )

    async def connect(self):
        """Инициализация подключения к базе данных."""
        # Здесь можно проверить подключение или подготовить сессию
        async with self._async_session() as session:
            await session.execute("SELECT 1")  # простой тест подключения

    async def fetch_batch(self, query: str, params: dict = None) -> List[Dict]:
        """
        Выполняет запрос и возвращает результаты как список словарей.
        query: SQL-запрос
        params: параметры для запроса
        """
        async with self._async_session() as session:
            result = await session.execute(query, params or {})
            rows = result.fetchall()
            # Конвертируем в список словарей
            return [dict(row) for row in rows]

    async def save_results(self, query: str, params_list: List[dict]):
        """
        Выполняет множественные вставки/обновления.
        query: SQL-запрос с плейсхолдерами
        params_list: список словарей с параметрами
        """
        async with self._async_session() as session:
            for params in params_list:
                await session.execute(query, params)
            await session.commit()
