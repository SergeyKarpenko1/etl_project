import pytest
import pandas as pd
from pathlib import Path
from service_llm_generator.clients.client import DBCSVClient

@pytest.mark.asyncio
async def test_fetch_batch(tmp_path: Path):
    # ───────────────
    # 1. Создаём тестовый CSV
    # ───────────────
    csv_path = tmp_path / "input.csv"
    df = pd.DataFrame([
        {"iid": 1, "text": "Привет"},
        {"iid": 2, "text": "Ты супер!"},
        {"iid": 3, "text": "Как дела?"}
    ])
    df.to_csv(csv_path, index=False)

    client = DBCSVClient(input_path=csv_path, output_path=tmp_path / "output.csv")

    # ───────────────
    # 2. Загружаем батч
    # ───────────────
    batch = await client.fetch_batch()
    assert isinstance(batch, list)
    assert len(batch) == 3
    assert batch[0]["text"] == "Привет"


@pytest.mark.asyncio
async def test_save_results(tmp_path: Path):
    # ───────────────
    # 1. Подготовка входных данных
    # ───────────────
    output_path = tmp_path / "output.csv"
    client = DBCSVClient(
        input_path=tmp_path / "input.csv",   # не используется
        output_path=output_path
    )

    batch = [
        {"iid": 1, "text": "Привет", "toxicity_score": 0.1},
        {"iid": 2, "text": "Ты супер!", "toxicity_score": 0.2},
    ]

    # ───────────────
    # 2. Сохраняем результаты
    # ───────────────
    await client.save_results(query=None, batch=batch)

    # ───────────────
    # 3. Проверяем сохранение
    saved_df = pd.read_csv(output_path)
    assert len(saved_df) == 2
    assert saved_df.iloc[0]["text"] == "Привет"
    assert saved_df.iloc[1]["toxicity_score"] == 0.2