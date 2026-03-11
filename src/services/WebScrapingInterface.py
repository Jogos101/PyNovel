
class WebScrapingInterface:
    # Metodo responsavel por coletar o titulo presente no capitulo
    def getTitulo(self, elemento):
        """Overridable"""
        pass

    # Metodo responsavel por formatar o conteudo em xhtml
    def format_as_xhtml(self, content_list):
        """Overridable"""
        pass

    # Metodo principal que processa o capitulo
    def runChapter(self, cap):
        """Overridable"""
        pass

    # Metodo responsavel por checar pelo proximo capitulo pelo button(capitulo sem padrao)
    def updateNextButton(self):
        """Overridable"""
        pass
    
    # Metodo responsavel por atualizar a url atual
    def atualizaUrl(self):
        """Overridable"""
        pass

    # Metodo responsavel por calcular a proxima url
    def getNextUrlPadrao(self):
        """Overridable"""
        pass

    # Metodo padrao responsavel por finalizar alguns web scrapers
    def endScraping(self):
        """Overridable"""
        pass