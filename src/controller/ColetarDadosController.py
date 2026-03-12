from entity.Livro import Livro
from entity.Fonte import Fonte
from pathlib import Path
import json
import inquirer

class ColetarDadosController:
    def __init__(self):
        pass

    def coletar(self):
        # Coletar o método de coleta de dados
        library = [
        inquirer.List('WebScraper',
            message="Qual método de coleta você deseja?",
            choices=['Request(recommended)', 'Selenium'],
        ),
        ]
        answers = inquirer.prompt(library)
        metodo = answers["WebScraper"]

        sources = [
        inquirer.List('Fonte',
            message="Qual fonte você deseja coletar?",
            choices=self.listarFontes(),
        ),
        ]
        answers = inquirer.prompt(sources)
        fonte_selecionada = answers["Fonte"]

        # titulo, autor, idioma
        livro = Livro(*self.getDadosLivro(fonte_selecionada))
        # url, url_padrao, total_capitulos, class_titulo, tag_titulo, class_conteudo, next_chap, next_end, tag_conteudo
        fonte = Fonte(*self.getDadosFonte(fonte_selecionada))

        print("Quantos capítulos deseja coletar? (Digite 0 para coletar todos)")
        total_capitulos = int(input())
        if total_capitulos > 0:
            fonte.total_capitulos = total_capitulos

        return (fonte, livro, metodo)
    
    def listarFontes(self):
        # Listar as fontes disponíveis
        base_path = Path(__file__).resolve().parent.parent.parent
        fontes_dir = base_path / "resources" / "sources"

        # Cria o diretório de saída se ele não existir
        fontes_dir.mkdir(parents=True, exist_ok=True)

        fontes = [f.stem for f in fontes_dir.glob("*.json") if f.stem != 'exemplo_source']
        return fontes
    
    def getDadosLivro(self, fonte_selecionada):
        # Carregar os dados do livro a partir do arquivo JSON
        base_path = Path(__file__).resolve().parent.parent.parent
        fonte_path = base_path / "resources" / "sources" / f"{fonte_selecionada}.json"

        with open(fonte_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return (data["Name"], data["autor"], data.get("idioma", "en"))
    
    def getDadosFonte(self, fonte_selecionada):
        # Carregar os dados da fonte a partir do arquivo JSON
        base_path = Path(__file__).resolve().parent.parent.parent
        fonte_path = base_path / "resources" / "sources" / f"{fonte_selecionada}.json"

        with open(fonte_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return (data["url_inicial"], data["url_padrao"], data["total_capitulos"], data["titulo"], data["conteudo"], data["next_chap"], data["next_disabled"], data["tag_conteudo"])