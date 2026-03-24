import inquirer # type: ignore
from services.resource_collector_service import ResourceCollectorService as ResourceCollector
from entity.livro import Livro
from entity.fonte import Fonte

class ColetarDadosController:
    def __init__(self):
        pass

    def coletar(self):
        resource_collector = ResourceCollector()

        # Coletar o método de coleta de dados
        library = [
        inquirer.List('WebScraper',
            message="Qual método de coleta você deseja?",
            choices=[
                'Request(recommended)'
            ],
        ),
        ]
        answers = inquirer.prompt(library)
        metodo = answers["WebScraper"]

        sources = [
        inquirer.List('Fonte',
            message="Qual fonte você deseja coletar?",
            choices=resource_collector.listar_fontes(),
        ),
        ]
        answers = inquirer.prompt(sources)
        fonte_selecionada = answers["Fonte"]

        # titulo, autor, idioma
        livro = Livro(*resource_collector.get_dados_livro(fonte_selecionada))
        # url, url_padrao, total_capitulos, class_titulo, tag_titulo, class_conteudo, next_chap, next_end, tag_conteudo
        fonte = Fonte(*resource_collector.get_dados_fonte(fonte_selecionada))

        print("Quantos capítulos deseja coletar? (Digite 0 para coletar todos)")
        total_capitulos = int(input())
        if total_capitulos > 0:
            fonte.total_capitulos = total_capitulos

        return (fonte, livro, metodo)