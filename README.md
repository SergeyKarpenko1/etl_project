# ETL: Toxicity Classification Pipeline

Асинхронный ETL-пайплайн, который забирает тексты из CSV, очищает их, прогоняет через русскоязычную BERT-модель токсичности и сохраняет результаты в новый CSV.

## Структура проекта
```
.
├─ main.py                         # Точка входа, сборка пайплайна
├─ src/service_llm_generator
│  ├─ clients/client.py            # Класс для чтения/записи CSV (эмуляция БД)
│  ├─ processors/preprocessor.py   # Очистка текста
│  ├─ processors/postprocessor.py  # Округление и финализация вывода модели
│  ├─ models/toxicity_classifier.py# Работа с BERT-моделью токсичности
│  ├─ workers/etl_pipeline.py      # Оркестрация батчевого ETL
│  └─ utils/constants.py           # Пути к входным/выходным данным
├─ data
│  ├─ raw/dirty_toxicity_data_large.csv      # Ожидаемый вход
│  └─ processed/clean_toxicity_data.csv      # Результат пайплайна
├─ tests
│  └─ unit/                        # Набор unit-тестов для ключевых компонентов
├─ Dockerfile
├─ Makefile
├─ pyproject.toml
└─ uv.lock
```

## Требования
- Python 3.12+
- pip или uv для установки зависимостей
- Доступ в интернет при первом запуске (скачивание модели `s-nlp/russian_toxicity_classifier` из Hugging Face)
- Наличие входного файла `data/raw/dirty_toxicity_data_large.csv`

## Установка (локально)
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .                   # подтянет зависимости из pyproject.toml
```

## Данные
- Вход: `data/raw/dirty_toxicity_data_large.csv` (колонка `text` обязательна).
- Выход: `data/processed/clean_toxicity_data.csv` создаётся/перезаписывается.
- Пути к файлам заданы в `src/service_llm_generator/utils/constants.py`. По умолчанию они ориентированы на путь `/app/...` внутри Docker-контейнера. Для локального запуска замените их на абсолютные пути к файлам в текущем репозитории или смонтируйте папку `data` в контейнер.

## Запуск
### Локально
1. Убедитесь, что пути в `src/service_llm_generator/utils/constants.py` указывают на реальные файлы (например, `data/raw/...` и `data/processed/...` в корне проекта).
2. Запустите:
```bash
make run
# или вручную:
PYTHONPATH=src python main.py
```

### Через Docker
1. Собрать образ:
```bash
docker build -t etl-toxicity .
```
2. Запустить, пробросив локальную папку данных в контейнер:
```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  etl-toxicity
```

## Тестирование
```bash
make test
# или
PYTHONPATH=src pytest tests -v
```

## Кратко о пайплайне
1. `DBCSVClient.fetch_batch` читает все строки из CSV.
2. `Preprocessor` приводит текст к нижнему регистру, убирает пунктуацию и лишние пробелы.
3. `ModelClient` токенизирует тексты и получает `toxicity_score`, `is_toxic`, `toxicity_label`.
4. `Postprocessor` округляет score до 2 знаков.
5. `DBCSVClient.save_results` сохраняет результат в выходной CSV.

## Полезные команды
- `make run` — запуск пайплайна (учитывает PYTHONPATH).
- `make test` — все тесты.
- `docker build -t etl-toxicity .` — сборка образа.
