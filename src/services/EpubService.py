import pypub
from pathlib import Path
from entity.Livro import Livro
from entity.Capitulo import Capitulo

class EpubService:
    def __init__(self, livro):
        self.livro = livro
        self.epub = pypub.Epub(self.livro.titulo, self.livro.autor, self.livro.idioma)

    def criarCapitulo(self, capitulo):
        # Cria o capítulo com conteúdo e título
        self.epub.add_chapter(pypub.Chapter(title=capitulo.titulo, content=capitulo.conteudo, url=capitulo.url))

    # ../../resources/books/{titulo_limpo}{versao}.epub
    def gerarEpub(self):
        # Define o caminho de saída para o arquivo EPUB
        base_path = Path(__file__).resolve().parent.parent.parent
        output_dir = base_path / "resources" / "books"

        # Cria o diretório de saída se ele não existir
        output_dir.mkdir(parents=True, exist_ok=True)

        # Controlar concorrência de nome de arquivo
        nome_arquivo = self.livro.getTituloLimpo()
        extensao = ".epub"
        caminho_arquivo = output_dir / f"{nome_arquivo}{extensao}"

        contador = 1
        while caminho_arquivo.exists():
            caminho_arquivo = output_dir / f"{nome_arquivo}_{contador}{extensao}"
            contador += 1

        self.epub.create(str(caminho_arquivo))
        print(f"Arquivo EPUB criado em: {caminho_arquivo}")