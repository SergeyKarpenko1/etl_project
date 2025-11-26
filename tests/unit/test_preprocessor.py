import pytest
from service_llm_generator.processors.preprocessor import Preprocessor

@pytest.fixture
def sample_batch():
    return [
        {"text": "Привет!!! Как дела??"},
        {"text": "  Это    тестовый ТЕКСТ123...   "},
        {"text": "Нейтральный текст :)"}
    ]

def test_clean_text():
    raw_text = "Привет!!! Как дела??"
    cleaned = Preprocessor.clean_text(raw_text)
    assert cleaned == "привет как дела"  # проверяем, что знаки препинания убраны и нижний регистр

def test_process_batch(sample_batch):
    processor = Preprocessor()
    processed = processor.process_batch(sample_batch)

    assert all("clean_text" in item for item in processed)  # у каждого элемента есть clean_text
    assert processed[0]["clean_text"] == "привет как дела"
    assert processed[1]["clean_text"] == "это тестовый текст123"
    assert processed[2]["clean_text"] == "нейтральный текст"