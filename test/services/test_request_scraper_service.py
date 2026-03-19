import unittest

from src.entity.fonte import Fonte
from src.entity.capitulo import Capitulo
from src.services.request_scraper_service import RequestScraperService


class TestRequestScraperService(unittest.TestCase):
    def setUp(self):
        self.request_scraper_service = RequestScraperService(
            Fonte(
                url_inicial="https://www.novel.com/book/titulo/Chapter-1",
                getTitulo={"id": "chapter-title"},
                getConteudo={"class": "chapter-content"},
            )
        )

if __name__ == "__main__":
    unittest.main()