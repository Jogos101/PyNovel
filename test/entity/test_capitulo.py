import unittest
from src.entity.capitulo import Capitulo

class TestCapitulo(unittest.TestCase):
    def setUp(self):
        self.capitulo = Capitulo(
            titulo="Chapter 1: Inicio",
            conteudo=b"<p>Conteudo do capitulo</p>",
            cap=1,
            url="https://site/chapter-1",
        )

    def test_atributos_basicos(self):
        self.assertEqual(self.capitulo.titulo, "Chapter 1: Inicio")
        self.assertEqual(self.capitulo.conteudo, b"<p>Conteudo do capitulo</p>")
        self.assertEqual(self.capitulo.cap, 1)
        self.assertEqual(self.capitulo.url, "https://site/chapter-1")

    def test_permite_conteudo_texto(self):
        capitulo_texto = Capitulo(
            titulo="Chapter 2",
            conteudo="<p>Texto em string</p>",
            cap=2,
            url="https://site/chapter-2",
        )

        self.assertEqual(capitulo_texto.conteudo, "<p>Texto em string</p>")
        self.assertEqual(capitulo_texto.cap, 2)


if __name__ == "__main__":
    unittest.main()