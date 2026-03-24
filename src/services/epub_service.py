import os
import ebooklib # type: ignore
from ebooklib import epub # type: ignore
import src.entity.livro
import src.entity.capitulo 
from pathlib import Path
import uuid

class EpubService:
    def __init__(self, livro):
        self.livro = livro
        self.lista_capitulos = []
        self.BASE_PATH = Path(__file__).resolve().parent.parent.parent
        self.ebook = None

    def getEbook(self, file):
        return epub.read_epub(file)
    
    def setEbook(self):
        if self.ebook is None:
            self.ebook = epub.EpubBook()

            if self.livro.cover is not None:
                self.set_cover()
            self.ebook.set_title(self.livro.titulo)
            self.ebook.set_language(self.livro.idioma)
            self.ebook.add_author(self.livro.autor)
            self.ebook.set_identifier(str(uuid.uuid4()))

    def set_style(self, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        c = epub.EpubItem()
        c.file_name = 'style/style.css'
        c.media_type = 'text/css'

        style_path = base_path / 'src' / 'layout' / 'style' / 'style.css'
        if not style_path.exists():
            raise FileNotFoundError(f"Arquivo de estilo não encontrado: {style_path}") 
        
        with open(style_path, 'r') as style_file:
            c.content = style_file.read()
        self.ebook.add_item(c)

    def set_cover(self):
        try:
            with open(self.livro.cover, 'rb') as cover_file:
                cover_data = cover_file.read()
                self.ebook.set_cover(os.path.basename(self.livro.cover), cover_data)
        except Exception as e:
            print(f"Erro ao definir a capa: {e}")

    def getSetEbook(self, file):
        if self.ebook is None:
            self.ebook = epub.read_epub(file)

    def setToc(self):
        self.ebook.toc = (self.lista_capitulos)
        self.ebook.spine = ['nav'] + self.lista_capitulos

    def criar_capitulo(self, capitulo):
        title=capitulo.titulo
        file_name=f'{capitulo.get_file_name()}.xhtml'
        lang= self.livro.idioma

        chapter = epub.EpubHtml(
            title=title,
            file_name=file_name,
            lang=lang,
            )
        
        chapter.set_content(self.formatar_conteudo(capitulo))
        
        self.ebook.add_item(chapter)
        self.lista_capitulos.append(chapter)

    def formatar_conteudo(self, capitulo, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        
        template_path = base_path / 'src' / 'layout' / 'content' / 'index.html'

        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        content = capitulo.conteudo.strip() if isinstance(capitulo.conteudo, str) else str(capitulo.conteudo)
        # Formatar o conteúdo para XHTML
        html_content = template.format(
            title=self.livro.titulo,
            chap_title=capitulo.titulo,
            content=content,
            url=capitulo.url
        )
        return html_content.encode('utf-8')

    def gerar_epub(self):
        self.set_style()

        self.setToc()

        self.ebook.add_item(epub.EpubNcx())
        self.ebook.add_item(epub.EpubNav())

        arquivo = self.set_arquivo()
        epub.write_epub(str(arquivo), self.ebook)

    def set_arquivo(self, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
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