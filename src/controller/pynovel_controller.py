import traceback

# from bs4 import BeautifulSoup
from src.services.file_path_service import FilePathService
from src.services.epub_service import EpubService
from tqdm import tqdm # type: ignore
from entity.livro import Livro
from entity.fonte import Fonte


class PyNovelController:
    def __init__(self, fonte: Fonte, livro: Livro, webscraping, epub):
        self.fonte = fonte
        self.livro = livro
        self.epub = epub
        self.webscraping = webscraping
        self.epub_service = EpubService(livro)
        self.file_path_service = FilePathService()

    def atualiza_url(self, cap):
        if cap < self.fonte.total_capitulos:
            self.webscraping.atualiza_url()
    
    def end_process(self):
        self.epub_service.gerar_epub()
        self.webscraping.end_scraping()

    def atualiza_epub(self, path):
        self.epub_service.atualiza_epub(path)
        self.webscraping.end_scraping()

    def create_epub(self):
        self.epub_service.setEbook()

        with tqdm(
            total=self.fonte.total_capitulos,
            desc="Processando",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} | Percorrido: {elapsed} | Restante: {remaining}",
        ) as pbar:
            for cap in range(1, self.fonte.total_capitulos + 1):
                try:
                    # Capturar o conteudo do capitulo pela url e registrar no epub
                    self.epub_service.criar_capitulo(self.webscraping.run_chapter(cap))

                    # Atualizar a barra de progresso
                    pbar.update(1)
                    pbar.refresh()

                    if not self.fonte.url_padrao:
                        # Seleciona o botão de próximo capítulo e verifica se está desativado
                        if not self.webscraping.update_next_button():
                            print(
                                "Botão de próximo capítulo está desativado. Finalizando a coleta de capítulos."
                            )
                            pbar.n = pbar.total  # Força o progresso a 100%
                            pbar.refresh()
                            break  # Sai do loop se o botão está desativado

                    self.atualiza_url(cap)
                except Exception as e:
                    print(f"Erro ao processar o capítulo {cap}: {e}")
                    traceback.print_exc()
                    break

            self.end_process()

    def update_epub(self):
        self.book_path = self.file_path_service.get_book_path(self.epub)
        self.epub_service.getSetEbook(self.book_path)
        ultimo_cap = self.epub_service.getUltimoCapitulo()
        capitulos_restantes = self.fonte.total_capitulos - ultimo_cap

        with tqdm(
            total=capitulos_restantes,
            desc="Atualizando",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} | Percorrido: {elapsed} | Restante: {remaining}",
        ) as pbar:
            for cap in range(ultimo_cap + 1, self.fonte.total_capitulos + 1):
                try:
                    # Capturar o conteudo do capitulo pela url e registrar no epub
                    self.epub_service.criar_capitulo(self.webscraping.run_chapter(cap))

                    # Atualizar a barra de progresso
                    pbar.update(1)
                    pbar.refresh()

                    if not self.fonte.url_padrao:
                        # Seleciona o botão de próximo capítulo e verifica se está desativado
                        if not self.webscraping.update_next_button():
                            print(
                                "Botão de próximo capítulo está desativado. Finalizando a coleta de capítulos."
                            )
                            pbar.n = pbar.total  # Força o progresso a 100%
                            pbar.refresh()
                            break  # Sai do loop se o botão está desativado

                    self.atualiza_url(cap)
                except Exception as e:
                    print(f"Erro ao processar o capítulo {cap}: {e}")
                    traceback.print_exc()
                    break

            self.atualiza_epub(self.book_path)