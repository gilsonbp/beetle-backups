FROM python:3.11-slim

RUN  apt-get update \
    && apt-get install -y wget make \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VIRTUALENVS_CREATE false
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/src"

WORKDIR /src
COPY poetry.lock pyproject.toml Makefile ./
COPY src/ ./src

RUN pip install --no-cache-dir -U pip poetry
RUN poetry install

CMD $DOCKER_CMD
