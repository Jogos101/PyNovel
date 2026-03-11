from entity.Fonte import Fonte
from entity.Capitulo import Capitulo
from factory.FindElementFactory import FindElementFactory
from services.WebScrapingInterface import WebScrapingInterface
import requests
from bs4 import BeautifulSoup
import re

class WebScrapingRequestService(WebScrapingInterface):
    def __init__(self, fonte: Fonte):
        self.fonte = fonte
        self.url = fonte.url_inicial
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }
        self.chapter_regex = re.compile(r'Chapter \d+(:|\s)?')

    # Função de limpeza do título
    def getTitulo(self, elemento):
        # Expressão regular para remover 'Chapter' e os números que seguem (opcionalmente com ':')
        # Retorna o título limpo
        return self.chapter_regex.sub('', elemento).strip()

    # Função para formatar o conteúdo como XHTML e converter para bytes
    def format_as_xhtml(self, content_list):
        parts = []

        for paragraph in content_list:
            text = paragraph.text
            escaped = (
                text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
            )
            parts.append(f"<p>{escaped}</p>")
        # Converte o conteúdo XHTML para bytes
        return "\n".join(parts).encode("utf-8")
    
    def runChapter(self, cap):
        response = self.session.get(self.url, headers=self.headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # container do capítulo
        contentElement = soup.find(
            "div",
            class_=self.fonte.class_conteudo
        )

        if contentElement is None:
            raise ValueError("Conteúdo do capítulo não encontrado")

        # título
        if self.fonte.class_titulo:
            tituloElement = soup.find(
                class_=self.fonte.class_titulo
            )
        else:
            tituloElement = contentElement.find(
                self.fonte.tag_titulo
            )

        if tituloElement is None:
            titulo = f"Chapter {cap}"
        else:
            titulo_limpo = self.getTitulo(tituloElement.get_text())

            if ":" not in titulo_limpo:
                titulo = f"Chapter {cap}: {titulo_limpo}"
            else:
                titulo = titulo_limpo

        # conteúdo
        conteudo = contentElement.find_all(self.fonte.tag_conteudo)
        texto_xhtml = self.format_as_xhtml(conteudo)

        return Capitulo(titulo, texto_xhtml, cap, self.url)
        
    def atualizaUrl(self):
        if self.fonte.url_padrao:
            self.getNextUrlPadrao()
        # else:
        #     self.url = self.fonte.next_button.get_attribute('href')

    def getNextUrlPadrao(self):
        match = re.search(r'chapter-(\d+)', self.url)

        if not match:
            raise ValueError("Não foi possível identificar o número do capítulo na URL")

        capitulo_atual = int(match.group(1))
        proximo_capitulo = capitulo_atual + 1

        self.url = self.url.replace(f"chapter-{capitulo_atual}", f"chapter-{proximo_capitulo}")