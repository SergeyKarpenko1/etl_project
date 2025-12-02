from typing import List, Dict
import re


class Preprocessor:
    """Класс для очистки и подготовки текста перед моделью."""

    @staticmethod
    def clean_text(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zа-я0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def process_batch(self, batch: List[Dict]) -> List[Dict]:
        for item in batch:
            item["clean_text"] = self.clean_text(item["text"])
        return batch
