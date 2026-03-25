from pathlib import Path

class FilePathService:
    def __init__(self):
        self.BASE_PATH = Path(__file__).resolve().parent.parent.parent

    def get_layout_content_path(self, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        layout_path = base_path / 'src' / 'layout' / 'content' / 'index.html'
        if not layout_path.exists():
            raise FileNotFoundError(f"Arquivo de layout não encontrado: {layout_path}")
        return layout_path
    
    def get_style_path(self, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        style_path = base_path / 'src' / 'layout' / 'style' / 'style.css'
        if not style_path.exists():
            raise FileNotFoundError(f"Arquivo de estilo não encontrado: {style_path}")
        return style_path
    
    def get_cover_path(self, source, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        cover_path = base_path / "resources" / "covers" / f"{source}.jpg"
        if not cover_path.exists():
            raise FileNotFoundError(f"Arquivo de capa não encontrado: {cover_path}")
        return cover_path
    
    def get_all_sources(self, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        fontes_dir = base_path / "resources" / "sources"
        fontes_dir.mkdir(parents=True, exist_ok=True)
        fontes = [f.stem for f in fontes_dir.glob("*.json") if f.stem != 'exemplo_source']
        return fontes
    
    def get_source_path(self, source, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        source_path = base_path / "resources" / "sources" / f"{source}.json"
        if not source_path.exists():
            raise FileNotFoundError(f"Arquivo de fonte não encontrado: {source_path}")
        return source_path
    
    def get_all_books(self, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        books_dir = base_path / "resources" / "books"
        books_dir.mkdir(parents=True, exist_ok=True)
        books = [f.stem for f in books_dir.glob("*.epub")]
        return books
    
    def get_book_path(self, book, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        book_path = base_path / "resources" / "books" / f"{book}.epub"
        if not book_path.exists():
            raise FileNotFoundError(f"Livro não encontrado: {book_path}")
        return book_path

    def get_book_output_path(self, base_path=None):
        if base_path is None:
            base_path = self.BASE_PATH
        output_dir = base_path / "resources" / "books"
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir