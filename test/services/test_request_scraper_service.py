import unittest

from src.entity.fonte import Fonte
from src.entity.capitulo import Capitulo
from src.services.request_scraper_service import RequestScraperService


class TestRequestScraperService(unittest.TestCase):
    def setUp(self):
        self.fonte = Fonte(
                url="https://site/chapter-1",
                url_padrao=True,
                total_capitulos=15,
                titulo={
                    "id": None,
                    "class": "char-titulo",
                    "tag": None,
                },
                conteudo={
                    "id": "char-conteudo",
                    "class": None,
                    "tag": None,
                },
                next_chap=None,
                next_disabled="disabled",
                tag_conteudo="p",
            )
        self.request_scraper_service = RequestScraperService(self.fonte)

        self.request_patcher = unittest.mock.patch("requests.get")

if __name__ == "__main__":
    unittest.main()