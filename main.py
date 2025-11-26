import asyncio
from service_llm_generator.workers.etl_pipeline import ETLPipeline
from service_llm_generator.clients.client import DBCSVClient

INPUT = "data/raw/dirty_toxicity_data_large.csv"
OUTPUT = "data/processed/clean_toxicity_data.csv"

async def main():
    db = DBCSVClient(input_path=INPUT, output_path=OUTPUT)
    pipeline = ETLPipeline(db_client=db)
    await pipeline.run()

if __name__ == "__main__":
    asyncio.run(main())