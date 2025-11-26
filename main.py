import asyncio
from service_llm_generator.workers.etl_pipeline import ETLPipeline
from service_llm_generator.clients.client import DBCSVClient
from service_llm_generator.utils.constants import RAW_DATA_PATH, PROCESSED_DATA_PATH


async def main():
    db = DBCSVClient(input_path=RAW_DATA_PATH, output_path=PROCESSED_DATA_PATH)
    pipeline = ETLPipeline(db_client=db)
    await pipeline.run()  # просто так, без аргументов

if __name__ == "__main__":
    asyncio.run(main())