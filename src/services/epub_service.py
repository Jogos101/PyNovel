import os
import uuid
from ebooklib import epub # type: ignore
from src.services.file_path_service import FilePathService

class EpubService:
    def __init__(self, livro):
        self.livro = livro
        self.lista_capitulos = []
        self.file_path_service = FilePathService()
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

    def set_style(self):
        c = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css"
        )

        style_path = self.file_path_service.get_style_path()
        
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
        template_path = self.file_path_service.get_layout_content_path()

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

    def set_arquivo(self):
        output_dir = self.file_path_service.get_book_output_path()

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