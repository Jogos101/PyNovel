# Versão do Python utilizada
FROM python:3.14-slim

# Instalação do Chromium para o Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Definição do diretório de trabalho
WORKDIR /app

# Cópia do arquivo de requisitos e instalação das dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cópia do código-fonte para o contêiner
COPY . .

# Comando para rodar a aplicação
CMD ["python", "src/main.py"]