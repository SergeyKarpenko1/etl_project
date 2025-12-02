from dataclasses import dataclass
from typing import Any, Dict, List, Sequence

import torch
from transformers import BertForSequenceClassification, BertTokenizer


@dataclass
class Prediction:
    score: float
    threshold: float
    label: str
    is_toxic: bool


class ToxicityModel:
    def __init__(self, model_name: str = "s-nlp/russian_toxicity_classifier"):
        self.model_name = model_name
        self._load()

    def _load(self) -> None:
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForSequenceClassification.from_pretrained(self.model_name)
        self.model.eval()

    def predict_scores(self, texts: Sequence[str]) -> List[float]:
        encoded = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**encoded).logits
            probs = torch.softmax(logits, dim=-1)
        return probs[:, 1].tolist()  # toxic score


class ModelClient:
    def __init__(self, model: ToxicityModel | None = None, threshold: float = 0.5):
        self.model = model or ToxicityModel()
        self.threshold = threshold

    def preprocess(self, batch: List[Dict]) -> List[str]:
        return [item["text"] for item in batch]

    def predict(self, batch: List[Dict]) -> List[Prediction]:
        texts = self.preprocess(batch)
        scores = self.model.predict_scores(texts)

        predictions: List[Prediction] = []
        for score in scores:
            is_toxic = score > self.threshold
            predictions.append(
                Prediction(
                    score=score,
                    threshold=self.threshold,
                    is_toxic=is_toxic,
                    label="TOXIC" if is_toxic else "SAFE",
                )
            )
        return predictions

    def predict_batch(self, batch: List[Dict]) -> List[Dict]:
        preds = self.predict(batch)
        for item, pred in zip(batch, preds):
            item["toxicity_score"] = pred.score
            item["is_toxic"] = int(pred.is_toxic)
            item["toxicity_label"] = pred.label
        return batch
