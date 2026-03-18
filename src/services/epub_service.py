import pypub # type: ignore
import entity.livro
import entity.capitulo 
from pathlib import Path

class EpubService:
    def __init__(self, livro):
        self.livro = livro
        self.epub = pypub.Epub(self.livro.titulo, self.livro.autor, self.livro.idioma, cover=self.livro.cover)

    def criar_capitulo(self, capitulo):
        # Cria o capítulo com conteúdo e título
        self.epub.add_chapter(pypub.Chapter(title=capitulo.titulo, content=capitulo.conteudo, url=capitulo.url))

    # ../../resources/books/{titulo_limpo}{versao}.epub
    def gerar_epub(self):
        arquivo = self.set_arquivo()

        self.epub.create(str(arquivo))
        print(f"Arquivo EPUB criado em: {arquivo}")

    def set_arquivo(self):
        base_path = Path(__file__).resolve().parent.parent.parent
        output_dir = base_path / "resources" / "books"
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