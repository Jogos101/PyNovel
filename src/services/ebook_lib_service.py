import os

import ebooklib # type: ignore
from ebooklib import epub # type: ignore
from src.services.epub_service import EpubService
import src.entity.livro
import src.entity.capitulo 
from pathlib import Path

class EbookLibService(EpubService):
    def __init__(self, livro):
        self.livro = livro
        self.lista_capitulos = []
        self.ebook = None

    def getEbook(self, file):
        return epub.read_epub(file)
    
    def setEbook(self):
        if self.ebook is None:
            self.ebook = epub.EpubBook()

    def getSetEbook(self, file):
        if self.ebook is None:
            self.ebook = epub.read_epub(file)

    def setToc(self):
        self.ebook.toc = (
            (epub.Section(self.livro.get_titulo_limpo()), self.lista_capitulos),
        )

    def criar_capitulo(self, capitulo):
        title=capitulo.titulo
        file_name=f'{capitulo.get_file_name()}.xhtml'
        content=capitulo.conteudo
        lang= self.livro.idioma

        chapter = epub.EpubHtml(
            title=title,
            file_name=file_name,
            content=content,
            lang=lang
            )
        self.ebook.add_item(chapter)
        self.lista_capitulos.append(chapter)

    def gerar_epub(self):
        self.setToc()
        arquivo = self.set_arquivo()
        epub.write_epub(str(arquivo), self.ebook)

    def set_arquivo(self, BASE_PATH=Path(__file__).resolve().parent.parent.parent):
        output_dir = BASE_PATH / "resources" / "books"
        output_dir.mkdir(parents=True, exist_ok=True)

        caminho_arquivo = self.controlar_concorrencia(output_dir)
        return caminho_arquivo
    
    def controlar_concorrencia(self, output_dir):
        # Controlar concorrência de nome de arquivo
        nome_arquivo = self.livro.get_titulo_limpo()
        extensao = ".epub"
        caminho_arquivo = output_dir / f"{nome_arquivo}{extensao}"

        contador = 1
        while caminho_arquivo.exists():
            caminho_arquivo = output_dir / f"{nome_arquivo}_{contador}{extensao}"
            contador += 1
        return caminho_arquivo