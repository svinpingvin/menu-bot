FROM python:3.11-slim

WORKDIR /app

RUN apt update && apt install -y libpq-dev gcc

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

COPY . .

CMD ["poetry", "run", "python", "main.py"]
