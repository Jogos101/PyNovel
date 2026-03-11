# PyNovel

PyNovel é um projeto desenvolvido para facilitar a manipulação e coleta de dados de livros, utilizando técnicas de web scraping e manipulação de arquivos EPUB. Este README fornece informações sobre a estrutura do projeto, como instalar e usar a aplicação.

## Estrutura do Projeto

O projeto possui a seguinte estrutura de diretórios:

```
PyNovel/
├──src/
│   ├── main.py                      # Ponto de entrada da aplicação
│   ├── teste.py                     # Testes ou exemplos de uso
│   ├── controller/
│   │   └── PyNovelController.py     # Controlador da lógica da aplicação
│   ├── entity/
│   │   ├── Capitulo.py              # Classe que representa um capítulo de um livro
│   │   ├── Fonte.py                 # Classe que representa a fonte de um livro ou capítulo
│   │   └── Livro.py                 # Classe que representa um livro
│   ├── factory/
│   │   ├── FindElementFactory.py     # Fábrica para encontrar elementos em interfaces
│   │   └── WebScraperFactory.py      # Fábrica para criar scrapers da web
│   └── services/
│       ├── EpubService.py            # Serviço para manipulação de arquivos EPUB
│       ├── RequestScraperService.py  # Serviço para requisições HTTP
│       ├── SeleniumScraperService.py # Serviço para scraping com Selenium
│       └── WebScrapingInterface.py   # Interface para serviços de scraping
├── reources/
│   └── books/                        # Local onde são armazenados os Epubs gerados
└── README.md                         # Documentação do projeto
```

## Instalação

Para instalar o PyNovel, siga os passos abaixo:

1. Clone o repositório:
   ```
   git clone https://github.com/Jogos101/PyNovel
   ```
2. Navegue até o diretório do projeto:
   ```
   cd PyNovel
   ```
3. Instale as dependências necessárias
   ```
   pip install tqdm
   pip install pypub3
   pip install selenium
   pip install requests
   pip install beautifulsoup4
   pip install inquirer
   ```

## Uso

Para executar a aplicação, utilize o seguinte comando:

```
python main.py
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.