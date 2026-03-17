# PyNovel

PyNovel é um projeto desenvolvido para facilitar a manipulação e coleta de dados de livros, utilizando técnicas de web scraping e manipulação de arquivos EPUB. Este README fornece informações sobre a estrutura do projeto, como instalar e usar a aplicação.

## Estrutura do Projeto

O projeto possui a seguinte estrutura de diretórios:

```
PyNovel/
├── src/
│   ├── main.py                        # Ponto de entrada da aplicação
│   ├── controller/
│   │   ├── ColetarDadosController.py  # Controlador para coleta de dados
│   │   └── PyNovelController.py       # Controlador da lógica da aplicação
│   ├── entity/
│   │   ├── Capitulo.py                # Classe que representa um capítulo de um livro
│   │   ├── Fonte.py                   # Classe que representa a fonte de um livro ou capítulo
│   │   └── Livro.py                   # Classe que representa um livro
│   ├── factory/
│   │   ├── FindElementFactory.py      # Fábrica para encontrar elementos em interfaces
│   │   └── WebScraperFactory.py       # Fábrica para criar scrapers da web
│   └── services/
│       ├── EpubService.py             # Serviço para manipulação de arquivos EPUB
│       ├── RequestScraperService.py   # Serviço para requisições HTTP
│       ├── SeleniumScraperService.py  # Serviço para scraping com Selenium
│       └── WebScrapingInterface.py    # Interface para servicos de scraping
├── resources/
│   └── books/                         # Local onde são armazenados os EPUBs gerados
├── .dockerignore                      # Evita copiar arquivos indesejados para o Docker
├── Dockerfile                         # Imagem da aplicação
├── docker-compose.yml                 # Orquestração local via Docker Compose
├── requirements.txt                   # Dependências Python
└── README.md                          # Documentação do projeto
```

## Instalação (execucao local)

1. Clone o repositório:

   ```bash
   git clone https://github.com/Jogos101/PyNovel
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd PyNovel
   ```

3. Instale as dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso (execucao local)

Na raiz do projeto, execute:

```bash
python src/main.py
```

## Uso com Docker Compose

Pre-requisito: Docker e Docker Compose instalados.

1. Na raiz do projeto, construa a imagem:

   ```bash
   # Build só da aplicação (target app)
   docker compose build app

   # Build só dos testes (target tests)
   docker compose build tests
   ```

2. Roda a aplicacao no terminal:

    ```bash
   # Rodar app
   docker compose run --rm app

   # Rodar suíte completa de testes (serviço tests)
   docker compose --profile test run --rm tests

   # Ver logs do app
   docker compose logs -f app
   ```


## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.