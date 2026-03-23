import re

class Capitulo:
    def __init__(self, titulo, conteudo, cap, url):
        self.titulo = titulo
        self.conteudo = conteudo
        self.cap = cap
        self.url = url

    def get_file_name(self):
        return re.sub(r'[\\/*?:"<>|]', "", self.titulo).replace(' ', '_')