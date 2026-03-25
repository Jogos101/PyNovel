import inquirer # type: ignore
from services.resource_collector_service import ResourceCollectorService as ResourceCollector
from src.services.file_path_service import FilePathService
from entity.livro import Livro
from entity.fonte import Fonte

class ColetarDadosController:
    def __init__(self):
        self.resource_collector = ResourceCollector()
        self.file_path = FilePathService()
        self.epub = None

    def coletar(self):
        operation_selected = self.seletor_operation()
        metodo = self.seletor_metodo()
        fonte, livro = self.seletor_dados(operation_selected)

        return (fonte, livro, metodo, self.operation, self.epub)

    def seletor_operation(self):
        print(" BEM VINDO(A) AO PYNOVEL! ")
        print("<------------------------>")
        operations = [
        inquirer.List('Operation',
            message="Qual operação deseja realizar?",
            choices=[
                'Criar um Epub do zero.',
                'Atualizar um Epub existente.'
            ],
        ),
        ]
        answer = inquirer.prompt(operations)

        return answer["Operation"]
    
    def seletor_metodo(self):
        # Coletar o método de coleta de dados
        library = [
        inquirer.List('WebScraper',
            message="Qual método de coleta você deseja utilizar?",
            choices=[
                'Request(recommended)'
            ],
        ),
        ]
        answers = inquirer.prompt(library)

        return answers["WebScraper"]
    
    def seletor_dados(self, operation):
        match operation:
            case 'Criar um Epub do zero.':
                self.operation = "CREATE"
                return self.seletor_fonte()
            case 'Atualizar um Epub existente.':
                self.operation = "UPDATE"
                return self.seletor_epub()
            case _:
                raise ValueError("Erro ao selecionar a operação.")

    def seletor_fonte(self):
        sources = [
        inquirer.List('Fonte',
            message="Qual fonte você deseja coletar?",
            choices=self.resource_collector.listar_fontes(),
        ),
        ]
        answers = inquirer.prompt(sources)
        fonte_selecionada = answers["Fonte"]

        # titulo, autor, idioma
        livro = Livro(*self.resource_collector.get_dados_livro(fonte_selecionada))
        # url, url_padrao, total_capitulos, class_titulo, tag_titulo, class_conteudo, next_chap, next_end, tag_conteudo
        fonte = Fonte(*self.resource_collector.get_dados_fonte(fonte_selecionada))

        print("Quantos capítulos deseja coletar? (Digite 0 para coletar todos)")
        total_capitulos = int(input())
        if total_capitulos > 0:
            fonte.total_capitulos = total_capitulos

        return (fonte, livro)

    def seletor_epub(self):
        books = [
            inquirer.List('Books',
                message="Qual livro deseja atualizar?",
                choices=self.resource_collector.listar_livros(),
            ),
        ]
        answers = inquirer.prompt(books)
        self.epub = answers["Books"]

        return self.seletor_fonte()
