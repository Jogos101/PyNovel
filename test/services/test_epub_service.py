import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

from src.entity.capitulo import Capitulo
from src.entity.livro import Livro
from src.services.epub_service import EpubService


class TestEpubService(unittest.TestCase):
    def setUp(self):
        self.livro = Livro("Titulo do Livro", "Autor do Livro", "pt-BR", "capa.jpg")

        self.epub_patcher = patch("src.services.epub_service.pypub.Epub", autospec=True)
        self.mock_epub_cls = self.epub_patcher.start()
        self.addCleanup(self.epub_patcher.stop)

        self.mock_epub_instance = MagicMock()
        self.mock_epub_cls.return_value = self.mock_epub_instance

        self.epub_service = EpubService(self.livro)

    def test_init_deve_criar_epub_com_dados_do_livro(self):
        self.mock_epub_cls.assert_called_once_with(
            "Titulo do Livro",
            "Autor do Livro",
            "pt-BR",
            cover="capa.jpg",
        )

    def test_criar_capitulo_deve_adicionar_chapter_ao_epub(self):
        capitulo = Capitulo(
            titulo="Capitulo 1",
            conteudo="<p>Conteudo</p>",
            cap=1,
            url="https://site/capitulo-1",
        )

        chapter_obj = object()
        with patch("src.services.epub_service.pypub.Chapter", return_value=chapter_obj) as mock_chapter:
            self.epub_service.criar_capitulo(capitulo)

        mock_chapter.assert_called_once_with(
            title="Capitulo 1",
            content="<p>Conteudo</p>",
            url="https://site/capitulo-1",
        )
        self.mock_epub_instance.add_chapter.assert_called_once_with(chapter_obj)

    def test_gerar_epub_deve_criar_arquivo_no_caminho_retornado(self):
        arquivo = Path("resources/books/livro.epub")

        with patch.object(self.epub_service, "set_arquivo", return_value=arquivo) as mock_set_arquivo:
            with patch("builtins.print") as mock_print:
                self.epub_service.gerar_epub()

        mock_set_arquivo.assert_called_once_with()
        self.mock_epub_instance.create.assert_called_once_with(str(arquivo))
        mock_print.assert_called_once_with(f"Arquivo EPUB criado em: {arquivo}")

    def test_set_arquivo_deve_criar_pasta_de_saida_e_retornar_caminho(self):
        with TemporaryDirectory() as tmp_dir:
            fake_service_file = Path(tmp_dir) / "src" / "services" / "epub_service.py"
            fake_service_file.parent.mkdir(parents=True, exist_ok=True)
            fake_service_file.touch()

            output_dir = Path(tmp_dir) / "resources" / "books"
            caminho_esperado = output_dir / "Titulo_do_Livro.epub"

            with patch("src.services.epub_service.__file__", str(fake_service_file)):
                with patch.object(
                    self.epub_service,
                    "controlar_concorrencia",
                    return_value=caminho_esperado,
                ) as mock_controlar:
                    resultado = self.epub_service.set_arquivo()

            self.assertTrue(output_dir.exists())
            self.assertEqual(resultado, caminho_esperado)
            mock_controlar.assert_called_once_with(output_dir)

    def test_controlar_concorrencia_deve_retornar_nome_sem_sufixo_quando_livre(self):
        with TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)

            caminho = self.epub_service.controlar_concorrencia(output_dir)

        self.assertEqual(caminho, output_dir / "Titulo_do_Livro.epub")

    def test_controlar_concorrencia_deve_incrementar_sufixo_quando_arquivo_existir(self):
        with TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            (output_dir / "Titulo_do_Livro.epub").touch()
            (output_dir / "Titulo_do_Livro_1.epub").touch()

            caminho = self.epub_service.controlar_concorrencia(output_dir)

        self.assertEqual(caminho, output_dir / "Titulo_do_Livro_2.epub")


if __name__ == "__main__":
    unittest.main()