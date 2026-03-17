# Versão do Python utilizada
FROM python:3.14-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

FROM base AS test
COPY . .
# Rodar apenas o teste de unidades
CMD ["python", "-m", "unittest", "discover", "-s", "test", "-p", "test_*.py", "-v"]


FROM base AS app
# Instalação do Chromium para o Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

COPY . .
# Comando para rodar a aplicação
CMD ["python", "src/main.py"]