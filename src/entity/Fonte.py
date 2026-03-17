class Fonte:
    def __init__(self, url, url_padrao, total_capitulos, titulo, conteudo, next_chap, next_disabled, tag_conteudo):
        self.url_inicial = url
        self.url_padrao = url_padrao
        # Quantidade de capítulos
        self.total_capitulos = total_capitulos
        # Dados HTML
        self.__titulo = titulo
        self.__conteudo = conteudo
        self.next_chap = next_chap
        self.next_end = next_disabled
        self.tag_conteudo = tag_conteudo

    def to_string(self):
        return f"URL Inicial: {self.url_inicial}\nURL Padrão: {self.url_padrao}\nTotal de Capítulos: {self.total_capitulos}\nTítulo: {self.get_titulo()}\nConteúdo: {self.get_conteudo()}\nNext Chap: {self.next_chap}\nNext Disabled: {self.next_end}"

    def get_titulo(self):
        titulo_filtrado = filter(lambda item: item[1] is not None, self.__titulo.items())
        titulo_dict = dict(titulo_filtrado)
        return titulo_dict
    
    def get_conteudo(self):
        conteudo_filtrado = filter(lambda item: item[1] is not None, self.__conteudo.items())
        conteudo_dict = dict(conteudo_filtrado)
        return conteudo_dict