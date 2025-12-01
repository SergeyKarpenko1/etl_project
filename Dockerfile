FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/
COPY src /app/src
COPY main.py /app/main.py

RUN pip install --no-cache-dir uv \
    && uv pip install --system .

CMD ["python", "main.py"]