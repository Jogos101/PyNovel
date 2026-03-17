
from abc import ABC, abstractmethod


class WebScrapingInterface(ABC):
    # Metodo responsavel por coletar o titulo presente no capitulo
    @abstractmethod
    def getTitulo(self, elemento):
        """Overridable"""
        pass

    # Metodo responsavel por formatar o conteudo em xhtml
    @abstractmethod
    def format_as_xhtml(self, content_list):
        """Overridable"""
        pass

    # Metodo principal que processa o capitulo
    @abstractmethod
    def runChapter(self, cap):
        """Overridable"""
        pass

    # Metodo responsavel por checar pelo proximo capitulo pelo button(capitulo sem padrao)
    @abstractmethod
    def updateNextButton(self):
        """Overridable"""
        pass
    
    # Metodo responsavel por atualizar a url atual
    @abstractmethod
    def atualizaUrl(self):
        """Overridable"""
        pass

    # Metodo responsavel por calcular a proxima url
    @abstractmethod
    def getNextUrlPadrao(self):
        """Overridable"""
        pass

    # Metodo padrao responsavel por finalizar alguns web scrapers
    @abstractmethod
    def endScraping(self):
        """Overridable"""
        pass