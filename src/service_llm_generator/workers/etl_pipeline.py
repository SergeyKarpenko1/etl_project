from typing import List, Dict
from service_llm_generator.clients.client import DBCSVClient
from service_llm_generator.processors.preprocessor import Preprocessor
from service_llm_generator.models.toxicity_classifier import ModelClient
from service_llm_generator.processors.postprocessor import Postprocessor


class ETLPipeline:
    """Асинхронный батчевый ETL-пайплайн."""

    def __init__(self, db_client: DBCSVClient):
        self.db_client = db_client
        self.preprocessor = Preprocessor()
        self.model = ModelClient()
        self.postprocessor = Postprocessor()

    async def run(self):
        batch: List[Dict] = await self.db_client.fetch_batch()

        if not batch:
            return

        batch = self.preprocessor.process_batch(batch)
        batch = self.model.predict_batch(batch)
        batch = self.postprocessor.process_batch(batch)

        await self.db_client.save_results(None, batch)
