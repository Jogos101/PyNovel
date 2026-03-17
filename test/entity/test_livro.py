import unittest
from src.entity.livro import Livro

class TestLivro(unittest.TestCase):
    def setUp(self):
        self.livro = Livro(
            titulo='Meu: Livro/"Teste"?',
            autor="Autor Exemplo",
            idioma="pt-BR",
            cover="/tmp/capa.jpg",
        )

    def test_atributos_basicos(self):
        self.assertEqual(self.livro.titulo, 'Meu: Livro/"Teste"?')
        self.assertEqual(self.livro.autor, "Autor Exemplo")
        self.assertEqual(self.livro.idioma, "pt-BR")
        self.assertEqual(self.livro.cover, "/tmp/capa.jpg")

    def test_get_titulo_limpo_remove_caracteres_invalidos_e_troca_espacos(self):
        self.assertEqual(self.livro.get_titulo_limpo(), "Meu_LivroTeste")

    def test_valores_padrao_quando_nao_informados(self):
        livro_padrao = Livro(titulo="Livro Simples", autor="Autor")

        self.assertEqual(livro_padrao.idioma, "en")
        self.assertIsNone(livro_padrao.cover)
        self.assertEqual(livro_padrao.get_titulo_limpo(), "Livro_Simples")


if __name__ == "__main__":
    unittest.main()