# Используем официальный образ Python
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock*

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["python", "main.py",]