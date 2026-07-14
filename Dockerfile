FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CORPUS_PATH=/app/data/starter_corpus
ENV EVAL_DATASET_PATH=/app/src/knowledge_agent/eval/dataset.jsonl

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data

RUN pip install --no-cache-dir .

CMD ["uvicorn", "knowledge_agent.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
