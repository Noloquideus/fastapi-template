FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install poetry==2.1.3 && poetry config virtualenvs.create false && poetry install --only main --no-root
RUN pip install granian

COPY . .

CMD ["granian", "--interface", "asgi", "--host", "0.0.0.0", "--port", "9000", "--workers", "4", "src.main:app"]
