# syntax=docker/dockerfile:1.7
FROM python:3.14-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
	pip install --no-cache-dir -r requirements.txt

FROM base AS test
COPY src ./src
COPY test ./test
COPY resources ./resources
# Rodar apenas os testes de unidade
CMD ["python", "-m", "unittest", "discover", "-s", "test", "-p", "test_*.py", "-v"]

FROM base AS app
COPY src ./src
COPY resources ./resources
CMD ["python", "src/main.py"]