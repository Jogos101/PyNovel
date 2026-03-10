class Fonte:
    def __init__(self, url, url_padrao, total_capitulos, class_titulo, tag_titulo, class_conteudo, next_chap, next_end, tag_conteudo):
        self.url_inicial = url
        self.url_padrao = url_padrao
        # Quantidade de capítulos
        self.total_capitulos = total_capitulos
        # Dados HTML
        self.class_titulo = class_titulo
        self.tag_titulo = tag_titulo
        self.class_conteudo = class_conteudo
        self.next_chap = next_chap
        self.next_end = next_end
        self.tag_conteudo = tag_conteudo

    # def getTitulo(self):
    #     titulo_filtrado = filter(lambda item: item[1] is not None, self.__titulo.items())
    #     titulo_dict = dict(titulo_filtrado)
    #     return titulo_dict
    
    # def getConteudo(self):
    #     conteudo_filtrado = filter(lambda item: item[1] is not None, self.__conteudo.items())
    #     conteudo_dict = dict(conteudo_filtrado)
    #     return conteudo_dict