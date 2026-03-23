import os
import ebooklib # type: ignore
from ebooklib import epub # type: ignore
from src.services.epub_service import EpubService
import src.entity.livro
import src.entity.capitulo 
from pathlib import Path
import uuid

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

            if self.livro.cover is not None:
                self.set_cover()
            self.ebook.set_title(self.livro.titulo)
            self.ebook.set_language(self.livro.idioma)
            self.ebook.add_author(self.livro.autor)
            self.ebook.set_identifier(str(uuid.uuid4()))

    def set_style(self, BASE_PATH=Path(__file__).resolve().parent.parent.parent):
        c = epub.EpubItem()
        c.file_name = 'style/style.css'
        c.media_type = 'text/css'

        style_path = BASE_PATH / 'src' / 'layout' / 'style' / 'style.css'
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

    def formatar_conteudo(self, capitulo):
        content = capitulo.conteudo.strip() if isinstance(capitulo.conteudo, str) else str(capitulo.conteudo)
        # Formatar o conteúdo para XHTML
        html_content = f'''
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta charset="UTF-8" />
                <link rel="stylesheet" type="text/css" href="style/style.css" />
            </head>
            <body>
                <h1>{capitulo.titulo}</h1>
                {content}
            </body>
            </html>
        '''
        return html_content.encode('utf-8')

    def gerar_epub(self):
        self.set_style()

        self.setToc()

        self.ebook.add_item(epub.EpubNcx())
        self.ebook.add_item(epub.EpubNav())

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