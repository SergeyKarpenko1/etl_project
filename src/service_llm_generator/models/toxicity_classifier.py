from typing import List, Dict
import torch
from transformers import BertTokenizer, BertForSequenceClassification

class ModelClient:
    """Класс для работы с русскоязычной моделью токсичности (BERT)."""

    def __init__(self, model_name: str = "s-nlp/russian_toxicity_classifier"):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name)
        self.model.eval()  # ставим в режим inference

    def predict_batch(self, batch: List[Dict]) -> List[Dict]:
        texts = [item["text"] for item in batch]

        # Токенизация батча
        encoded = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**encoded)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)
            # Предположим, что модель выдаёт [SAFE, TOXIC]
            toxic_scores = probs[:, 1].tolist()

        # Добавляем предсказания в батч
        for item, score in zip(batch, toxic_scores):
            item["toxicity_score"] = score
            item["is_toxic"] = 1 if score > 0.5 else 0
            item["toxicity_label"] = "TOXIC" if item["is_toxic"] else "SAFE"

        return batch