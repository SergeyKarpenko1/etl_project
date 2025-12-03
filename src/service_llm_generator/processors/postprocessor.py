from typing import List, Dict


class Postprocessor:
    """Преобразует сырые предсказания модели в удобный формат."""

    def process_batch(self, batch: List[Dict]) -> List[Dict]:
        for item in batch:
            item["toxicity_score"] = round(float(item["toxicity_score"]), 2)
        return batch
