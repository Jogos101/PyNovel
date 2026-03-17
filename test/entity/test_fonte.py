import unittest
from src.entity.fonte import Fonte

class TestFonte(unittest.TestCase):
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

    def test_get_titulo_filtra_campos_none(self):
        self.assertEqual(self.fonte.get_titulo(), {"class": "char-titulo"})

    def test_get_conteudo_filtra_campos_none(self):
        self.assertEqual(self.fonte.get_conteudo(), {"id": "char-conteudo"})

    def test_atributos_basicos(self):
        self.assertEqual(self.fonte.url_inicial, "https://site/chapter-1")
        self.assertTrue(self.fonte.url_padrao)
        self.assertEqual(self.fonte.total_capitulos, 15)
        self.assertEqual(self.fonte.tag_conteudo, "p")


if __name__ == "__main__":
    unittest.main()