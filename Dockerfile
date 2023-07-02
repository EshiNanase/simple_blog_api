FROM python:3.11.4-alpine3.18

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini .
COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install
