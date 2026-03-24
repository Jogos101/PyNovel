
class PyNovelApplication:
    def __init__(self, coletar_dados_controller, webscraper_factory, epub_service, pynovel_controller):
        self.coletar_dados_controller = coletar_dados_controller
        self.webscraper_factory = webscraper_factory
        self.epub_service = epub_service
        self.pynovel_controller = pynovel_controller

    def run(self):
        fonte, livro, metodo = self.coletar_dados_controller.coletar()
        webscraping = self.webscraper_factory(metodo, fonte).get_web_scraper()
        epub = self.epub_service(livro)

        fluxo = self.pynovel_controller(
            fonte= fonte, 
            livro= livro, 
            webscraping= webscraping,
            epub= epub
        )
        fluxo.execute()