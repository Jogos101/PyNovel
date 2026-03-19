from pathlib import Path
import json
from src.services.resource_collector_service import ResourceCollectorService
from tempfile import TemporaryDirectory
import unittest

class TestResourceCollectorService(unittest.TestCase):
    def setUp(self):
        self.fonte = {
            "Name": "Nome do livro",
            "autor": "Autor do livro",
            "idioma": "en",
            "url_inicial": "https://sitedolivro/titulodolivro/chapter-1",
            "total_capitulos": 15,
            "titulo": {
                "id": None,
                "class": "char-titulo",
                "tag": None
            },
            "conteudo": {
                "id": "char-conteudo",
                "class": None,
                "tag": None
            },
            "url_padrao": True,
            "next_chap": None,
            "next_disabled": "disabled",
            "tag_conteudo": "p"
        }

    def test_listar_fontes_deve_retornar_lista_de_fontes(self):
        with TemporaryDirectory() as tmp_dir:
            # Configurar o ambiente de teste
            fontes_dir = Path(tmp_dir) / "resources" / "sources"

            fontes_dir.mkdir(parents=True, exist_ok=True)
            (fontes_dir / "exemplo_source.json").touch()
            (fontes_dir / "fonte1.json").touch()
            (fontes_dir / "fonte2.json").touch()

            service = ResourceCollectorService()
            fontes = service.listar_fontes(Path(tmp_dir))
            self.assertIn("fonte1", fontes)
            self.assertIn("fonte2", fontes)
            self.assertNotIn("exemplo_source", fontes)
            self.assertEqual(len(fontes), 2)
    
    def test_get_dados_livro_deve_retornar_dados_do_livro(self):
        with TemporaryDirectory() as tmp_dir:
            # Configurar o ambiente de teste
            fontes_dir = Path(tmp_dir) / "resources" / "sources"

            fontes_dir.mkdir(parents=True, exist_ok=True)
            (fontes_dir / "fonte1.json").touch()

            fonte_path = fontes_dir / "fonte1.json"

            with open(fonte_path, 'w', encoding='utf-8') as file:
                json.dump(self.fonte, file, indent=4)

            cover_dir = Path(tmp_dir) / "resources" / "covers"
            cover_dir.mkdir(parents=True, exist_ok=True)
            (cover_dir / "fonte1.jpg").touch()

            service = ResourceCollectorService()
            dados = service.get_dados_livro("fonte1", Path(tmp_dir))

            self.assertIn("Nome do livro", dados)
            self.assertIn("Autor do livro", dados)
            self.assertIn("en", dados)
            self.assertIsNotNone(dados[3])

    def test_get_dados_fonte_deve_retornar_dados_da_fonte(self):
        with TemporaryDirectory() as tmp_dir:
            # Configurar o ambiente de teste
            fontes_dir = Path(tmp_dir) / "resources" / "sources"

            fontes_dir.mkdir(parents=True, exist_ok=True)
            (fontes_dir / "fonte1.json").touch()

            fonte_path = fontes_dir / "fonte1.json"

            with open(fonte_path, 'w', encoding='utf-8') as file:
                json.dump(self.fonte, file, indent=4)

            service = ResourceCollectorService()
            dados = service.get_dados_fonte("fonte1", Path(tmp_dir))

            self.assertIn("https://sitedolivro/titulodolivro/chapter-1", dados)
            self.assertIn(True, dados)
            self.assertEqual(15, dados[2])
            self.assertIn("char-titulo", dados[3]["class"])
            self.assertIn("char-conteudo", dados[4]["id"])
            self.assertIn("p", dados[7])
            self.assertIn("disabled", dados[6])

if __name__ == "__main__":
    unittest.main()