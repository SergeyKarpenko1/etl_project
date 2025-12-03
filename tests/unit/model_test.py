import pytest
import torch
from unittest.mock import Mock, patch
from service_llm_generator.models.toxicity_classifier import ModelClient


@pytest.mark.parametrize(
    "texts,expected_labels",
    [
        (["Привет, ты супер"], ["SAFE"]),
        (["Ты ужасный человек"], ["TOXIC"]),
    ],
)
def test_predict_batch_with_mock(texts, expected_labels):
    batch = [{"text": t} for t in texts]

    # Мокаем токенизатор
    mock_tokenizer = Mock()
    mock_tokenizer.return_value = {
        "input_ids": torch.tensor([[0, 1]]),
        "attention_mask": torch.tensor([[1, 1]]),
    }

    # Мокаем модель
    mock_model = Mock()

    # Логиты как тензор, а не список
    if texts[0] == "Привет, ты супер":
        mock_model.return_value.logits = torch.tensor([[2.0, 1.0]])  # SAFE > TOXIC
    else:
        mock_model.return_value.logits = torch.tensor([[0.5, 3.0]])  # TOXIC > SAFE

    with (
        patch(
            "service_llm_generator.models.toxicity_classifier.BertTokenizer.from_pretrained",
            return_value=mock_tokenizer,
        ),
        patch(
            "service_llm_generator.models.toxicity_classifier.BertForSequenceClassification.from_pretrained",
            return_value=mock_model,
        ),
    ):
        client = ModelClient(model_name="mock-model")
        result = client.predict_batch(batch)

        # Проверяем, что батч получил новые поля
        for item, expected_label in zip(result, expected_labels):
            assert "toxicity_score" in item
            assert "is_toxic" in item
            assert "toxicity_label" in item
            assert item["toxicity_label"] == expected_label
