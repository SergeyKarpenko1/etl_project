import pandas as pd
from typing import List, Dict


class DBCSVClient:
    """
    Заменяет реальную БД, имитируя fetch/save через CSV-файл.
    """

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

    async def fetch_batch(self, query: str = None) -> List[Dict]:
        """
        Игнорируем query — CSV не требует SQL.
        """
        df = pd.read_csv(self.input_path)
        return df.to_dict(orient="records")

    async def save_results(self, query: str, batch: List[Dict]):
        df = pd.DataFrame(batch)
        df.to_csv(self.output_path, index=False)
