class Livro:
    def __init__(self, titulo, autor, idioma='en'):
        self.titulo = titulo
        self.autor = autor
        self.idioma = idioma
        self.arquivo = f"../books/{titulo.replace(' ', '_')}"