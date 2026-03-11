from services.SeleniumScraperService import SeleniumScraperService
from services.RequestScraperService import RequestScraperService

class WebScraperFactory:
    def __init__(self, metodo, fonte):
        self.metodo = metodo
        self.fonte = fonte

    def getWebScraper(self):
        match self.metodo:
            case 'Selenium':
                print("Running Selenium library")
                return SeleniumScraperService(self.fonte)
            case 'Request':
                print("Running Request library")
                return RequestScraperService(self.fonte)
            case _:
                raise ValueError("Não foi possível identificar o método de Web Scraping.")