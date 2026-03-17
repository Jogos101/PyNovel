import re

class Livro:
    def __init__(self, titulo, autor, idioma='en', cover=None):
        self.titulo = titulo
        self.autor = autor
        self.idioma = idioma
        self.cover = cover

    def get_titulo_limpo(self):
        # Limpa o título para evitar caracteres inválidos em nomes de arquivos
        return re.sub(r'[\\/*?:"<>|]', "", self.titulo).replace(' ', '_')