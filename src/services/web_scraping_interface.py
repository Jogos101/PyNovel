
from abc import ABC, abstractmethod


class WebScrapingInterface(ABC):
    # Metodo responsavel por coletar o titulo presente no capitulo
    @abstractmethod
    def get_titulo(self, elemento):
        """Overridable"""
        pass

    # Metodo responsavel por formatar o conteudo em xhtml
    @abstractmethod
    def format_as_xhtml(self, content_list):
        """Overridable"""
        pass

    # Metodo principal que processa o capitulo
    @abstractmethod
    def run_chapter(self, cap):
        """Overridable"""
        pass

    # Metodo responsavel por checar pelo proximo capitulo pelo button(capitulo sem padrao)
    @abstractmethod
    def update_next_button(self):
        """Overridable"""
        pass
    
    # Metodo responsavel por atualizar a url atual
    @abstractmethod
    def atualiza_url(self):
        """Overridable"""
        pass

    # Metodo responsavel por calcular a proxima url
    @abstractmethod
    def get_next_url_padrao(self):
        """Overridable"""
        pass

    # Metodo padrao responsavel por finalizar alguns web scrapers
    @abstractmethod
    def end_scraping(self):
        """Overridable"""
        pass