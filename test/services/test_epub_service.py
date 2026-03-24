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
        self.epub_service = EpubService(self.livro)

    def test_setEbook_deve_inicializar_epub_com_metadados(self):
        mock_book = MagicMock()

        with patch("src.services.epub_service.epub.EpubBook", return_value=mock_book) as mock_book_cls:
            with patch.object(self.epub_service, "set_cover") as mock_set_cover:
                with patch("src.services.epub_service.uuid.uuid4", return_value="uuid-fixo"):
                    self.epub_service.setEbook()

        mock_book_cls.assert_called_once_with()
        mock_set_cover.assert_called_once_with()
        mock_book.set_title.assert_called_once_with("Titulo do Livro")
        mock_book.set_language.assert_called_once_with("pt-BR")
        mock_book.add_author.assert_called_once_with("Autor do Livro")
        mock_book.set_identifier.assert_called_once_with("uuid-fixo")

    def test_setEbook_nao_deve_recriar_objeto_quando_ja_inicializado(self):
        self.epub_service.ebook = MagicMock()

        with patch("src.services.epub_service.epub.EpubBook") as mock_book_cls:
            self.epub_service.setEbook()

        mock_book_cls.assert_not_called()

    def test_criar_capitulo_deve_adicionar_chapter_ao_epub(self):
        self.epub_service.ebook = MagicMock()

        capitulo = Capitulo(
            titulo="Capitulo 1",
            conteudo="<p>Conteudo</p>",
            cap=1,
            url="https://site/capitulo-1",
        )

        chapter_obj = MagicMock()
        with patch("src.services.epub_service.epub.EpubHtml", return_value=chapter_obj) as mock_epub_html:
            with patch.object(self.epub_service, "formatar_conteudo", return_value=b"<html></html>"):
                self.epub_service.criar_capitulo(capitulo)

        mock_epub_html.assert_called_once_with(
            title="Capitulo 1",
            file_name="Capitulo_1.xhtml",
            lang="pt-BR",
        )
        chapter_obj.set_content.assert_called_once_with(b"<html></html>")
        self.epub_service.ebook.add_item.assert_called_once_with(chapter_obj)
        self.assertEqual(self.epub_service.lista_capitulos, [chapter_obj])

    def test_formatar_conteudo_deve_injetar_dados_no_template(self):
        capitulo = Capitulo(
            titulo="Capitulo 1",
            conteudo="<p>Conteudo</p>",
            cap=1,
            url="https://site/capitulo-1",
        )

        with TemporaryDirectory() as tmp_dir:
            template_path = Path(tmp_dir) / "template.xhtml"
            template_path.write_text(
                "<h1>{title}</h1><h2>{chap_title}</h2><article>{content}</article><a href='{url}'>fonte</a>",
                encoding="utf-8",
            )

            with patch.object(self.epub_service.file_path_service, "get_layout_content_path", return_value=template_path):
                resultado = self.epub_service.formatar_conteudo(capitulo)

        texto = resultado.decode("utf-8")
        self.assertIn("Titulo do Livro", texto)
        self.assertIn("Capitulo 1", texto)
        self.assertIn("<p>Conteudo</p>", texto)
        self.assertIn("https://site/capitulo-1", texto)

    def test_gerar_epub_deve_montar_estrutura_e_escrever_arquivo(self):
        self.epub_service.ebook = MagicMock()
        arquivo = Path("resources/books/livro.epub")

        with patch.object(self.epub_service, "set_style") as mock_set_style:
            with patch.object(self.epub_service, "setToc") as mock_set_toc:
                with patch.object(self.epub_service, "set_arquivo", return_value=arquivo) as mock_set_arquivo:
                    with patch("src.services.epub_service.epub.EpubNcx", return_value="ncx"):
                        with patch("src.services.epub_service.epub.EpubNav", return_value="nav"):
                            with patch("src.services.epub_service.epub.write_epub") as mock_write_epub:
                                self.epub_service.gerar_epub()

        mock_set_style.assert_called_once_with()
        mock_set_toc.assert_called_once_with()
        mock_set_arquivo.assert_called_once_with()
        self.epub_service.ebook.add_item.assert_any_call("ncx")
        self.epub_service.ebook.add_item.assert_any_call("nav")
        mock_write_epub.assert_called_once_with(str(arquivo), self.epub_service.ebook)

    def test_set_arquivo_deve_usar_servico_de_caminho_e_controle_de_concorrencia(self):
        output_dir = Path("resources/books")
        caminho_esperado = output_dir / "Titulo_do_Livro.epub"

        with patch.object(self.epub_service.file_path_service, "get_book_output_path", return_value=output_dir):
            with patch.object(self.epub_service, "controlar_concorrencia", return_value=caminho_esperado) as mock_controlar:
                resultado = self.epub_service.set_arquivo()

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