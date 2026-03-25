from factory.web_scraper_factory import WebScraperFactory
from factory.operation_factory import OperationFactory


class PyNovelApplication:
    def __init__(self, coletar_dados_controller, pynovel_controller):
        self.coletar_dados_controller = coletar_dados_controller
        self.pynovel_controller = pynovel_controller
        self.webscraper_factory = WebScraperFactory
        self.operation_factory = OperationFactory

    def run(self):
        fonte, livro, metodo, operation, epub = self.coletar_dados_controller.coletar()
        webscraping = self.webscraper_factory(metodo, fonte).get_web_scraper()

        fluxo = self.pynovel_controller(
            fonte= fonte, 
            livro= livro, 
            webscraping= webscraping,
            epub= epub
        )
        self.operation_factory(fluxo, operation).get_fluxo()