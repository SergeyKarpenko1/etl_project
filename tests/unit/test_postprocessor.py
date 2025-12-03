import pytest
from service_llm_generator.processors.postprocessor import Postprocessor


def test_postprocessor_rounds_scores():
    post = Postprocessor()
    batch = [
        {"text": "пример", "toxicity_score": 0.12345},
        {"text": "пример2", "toxicity_score": 0.98765},
    ]

    result = post.process_batch(batch)

    assert result[0]["toxicity_score"] == 0.12
    assert result[1]["toxicity_score"] == 0.99


def test_postprocessor_handles_string_scores():
    post = Postprocessor()
    batch = [{"text": "пример", "toxicity_score": "0.6789"}]

    result = post.process_batch(batch)

    assert result[0]["toxicity_score"] == 0.68


def test_postprocessor_preserves_other_fields():
    post = Postprocessor()
    batch = [
        {
            "id": 10,
            "text": "тест",
            "toxicity_score": 0.5566,
            "is_toxic": 1,
            "extra": "value",
        }
    ]

    result = post.process_batch(batch)

    assert result[0]["id"] == 10
    assert result[0]["text"] == "тест"
    assert result[0]["is_toxic"] == 1
    assert result[0]["extra"] == "value"
    assert result[0]["toxicity_score"] == 0.56


def test_postprocessor_empty_batch():
    post = Postprocessor()
    batch = []

    result = post.process_batch(batch)

    assert result == []


def test_postprocessor_raises_on_missing_score():
    post = Postprocessor()
    batch = [{"text": "пример"}]  # нет toxicity_score

    with pytest.raises(KeyError):
        post.process_batch(batch)
