import traceback
# from bs4 import BeautifulSoup
from tqdm import tqdm
from entity.Livro import Livro
from entity.Capitulo import Capitulo
from entity.Fonte import Fonte
from services.EpubService import EpubService
from services.WebScrapingService import WebScrapingService
from services.WebScrapingRequestService import WebScrapingRequestService

class PyNovelController:
    def __init__(self, fonte, livro):
        self.fonte = fonte
        self.livro = livro
        self.epub = EpubService(livro)
        self.webscraping = WebScrapingRequestService(fonte)

    def start(self):
        total_capitulos = self.fonte.total_capitulos

        with tqdm(total=total_capitulos, desc="Processando", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} | Percorrido: {elapsed} | Restante: {remaining}") as pbar:
            for cap in range(1, total_capitulos + 1):
                try:
                    # Capturar o conteudo do capitulo pela url e registrar no epub
                    self.epub.criarCapitulo(self.webscraping.runChapter(cap))

                    # tqdm.write(f'[{titulo}] concluído')
                    # Atualizar a barra de progresso
                    pbar.update(1)
                    pbar.refresh()

                    # if self.fonte.url_padrao == False: 
                    #     # Seleciona o botão de próximo capítulo e verifica se está desativado
                    #     if self.webscraping.updateNextButton() == False:
                    #         print("Botão de próximo capítulo está desativado. Finalizando a coleta de capítulos.")
                    #         pbar.n = pbar.total  # Força o progresso a 100%
                    #         pbar.refresh()
                    #         break  # Sai do loop se o botão está desativado

                    # Atualiza a URL para o próximo capítulo
                    if cap < total_capitulos:
                        self.webscraping.atualizaUrl()
                except Exception as e:
                        print(f"Erro ao processar o capítulo {cap}: {e}")
                        traceback.print_exc()
                        break
            self.epub.gerarEpub()
            # self.webscraping.endScraping()
