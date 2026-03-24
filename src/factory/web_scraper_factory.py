from services.request_scraper_service import RequestScraperService

class WebScraperFactory:
    def __init__(self, metodo, fonte):
        self.metodo = metodo
        self.fonte = fonte

    def get_web_scraper(self):
        match self.metodo:
            case 'Request(recommended)':
                print("Running Request library")
                return RequestScraperService(self.fonte)
            case _:
                raise ValueError("Não foi possível identificar o método de Web Scraping.")