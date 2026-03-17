import traceback

# from bs4 import BeautifulSoup
from tqdm import tqdm
from entity.Livro import Livro
from entity.Capitulo import Capitulo
from entity.Fonte import Fonte
from services.epub_service import EpubService
from factory.WebScraperFactory import WebScraperFactory


class PyNovelController:
    def __init__(self, fonte: Fonte, livro: Livro, webscraping, epub):
        self.fonte = fonte
        self.livro = livro
        self.epub = epub
        self.webscraping = webscraping

    def execute(self):
        with tqdm(
            total=self.fonte.total_capitulos,
            desc="Processando",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} | Percorrido: {elapsed} | Restante: {remaining}",
        ) as pbar:
            for cap in range(1, self.fonte.total_capitulos + 1):
                try:
                    # Capturar o conteudo do capitulo pela url e registrar no epub
                    self.epub.criar_capitulo(self.webscraping.runChapter(cap))

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

    def atualiza_url(self, cap):
        if cap < self.fonte.total_capitulos:
            self.webscraping.atualiza_url()
    
    def end_process(self):
        self.epub.gerar_epub()
        self.webscraping.end_scraping()
