import pytest
from unittest.mock import AsyncMock, Mock, patch, MagicMock
from service_llm_generator.clients.client import DBClient


@pytest.mark.asyncio
async def test_fetch_batch_with_mock():
    with patch(
        "service_llm_generator.clients.client.create_async_engine"
    ) as mock_engine:
        client = DBClient(dsn="postgresql+asyncpg://user:pass@localhost/test")

        # Мокаем асинхронную сессию
        mock_session = AsyncMock()
        mock_execute_result = Mock()

        # Создаём mock объекты строк, которые ведут себя как словари
        mock_row1 = MagicMock()
        mock_row1.__iter__ = Mock(return_value=iter(["id", "text"]))
        mock_row1.__getitem__ = Mock(
            side_effect=lambda key: {"id": 1, "text": "example 1"}[key]
        )
        mock_row1.keys = Mock(return_value=["id", "text"])

        mock_row2 = MagicMock()
        mock_row2.__iter__ = Mock(return_value=iter(["id", "text"]))
        mock_row2.__getitem__ = Mock(
            side_effect=lambda key: {"id": 2, "text": "example 2"}[key]
        )
        mock_row2.keys = Mock(return_value=["id", "text"])

        mock_execute_result.fetchall = Mock(return_value=[mock_row1, mock_row2])
        mock_session.execute.return_value = mock_execute_result

        client._async_session = Mock(
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session))
        )

        # Вызываем метод с правильными аргументами
        query = "SELECT id, text FROM table"
        batch = await client.fetch_batch(query=query)

        # Проверяем результат
        assert isinstance(batch, list)
        assert len(batch) == 2
        assert batch[0]["id"] == 1
        assert batch[1]["text"] == "example 2"


@pytest.mark.asyncio
async def test_save_results_with_mock():
    with patch(
        "service_llm_generator.clients.client.create_async_engine"
    ) as mock_engine:
        client = DBClient(dsn="postgresql+asyncpg://user:pass@localhost/test")

        # SQL запрос с плейсхолдерами
        query = "INSERT INTO results (id, clean_text, toxicity_score) VALUES (:id, :clean_text, :toxicity_score)"

        # Список параметров для вставки
        params_list = [
            {"id": 1, "clean_text": "clean", "toxicity_score": "0.1"},
            {"id": 2, "clean_text": "clean2", "toxicity_score": "0.9"},
        ]

        # Мокаем сессию
        mock_session = AsyncMock()
        client._async_session = Mock(
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session))
        )

        # Вызываем метод с правильными аргументами
        await client.save_results(query=query, params_list=params_list)

        # Проверяем, что execute вызывался столько раз, сколько элементов в params_list
        assert mock_session.execute.call_count == len(params_list)
        # Проверяем, что commit был вызван
        mock_session.commit.assert_awaited()
