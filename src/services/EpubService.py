import pypub
from entity.Livro import Livro
from entity.Capitulo import Capitulo

class EpubService:
    def __init__(self, livro):
        self.livro = livro
        self.epub = pypub.Epub(self.livro.titulo, self.livro.autor, self.livro.idioma)

    def criarCapitulo(self, capitulo):
        # Cria o capítulo com conteúdo e título
        self.epub.add_chapter(pypub.Chapter(title=capitulo.titulo, content=capitulo.conteudo, url=capitulo.url))

    def gerarEpub(self):
        # self.epub.create(self.livro.arquivo)
        self.epub.create()