from entity.Fonte import Fonte
from entity.Capitulo import Capitulo
from factory.FindElementFactory import FindElementFactory
from services.WebScrapingInterface import WebScrapingInterface
import requests
from bs4 import BeautifulSoup
import re
import time


class RequestScraperService(WebScrapingInterface):
    def __init__(self, fonte: Fonte):
        self.fonte = fonte
        self.url = fonte.url_inicial
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.chapter_regex = re.compile(r"Chapter \d+(:|\s)?")

    def getTitulo(self, elemento):
        # 1. Regex que captura: "Chapter", espaço, números (ou intervalos como 20-18) 
        # e qualquer combinação de ": ", " - " ou espaços que venham depois.
        # A flag re.IGNORECASE garante que pegue 'chapter' ou 'Chapter'.
        pattern = re.compile(r"Chapter\s+\d+(\s*-\s*\d+)?[:\s-]*", re.IGNORECASE)
        
        titulo_limpo = elemento.strip()
        
        # 2. Removemos o padrão repetidamente. 
        # Isso resolve casos como "Chapter 1: Chapter 1: Título"
        while pattern.match(titulo_limpo):
            novo_titulo = pattern.sub("", titulo_limpo, count=1).strip()
            # Se a limpeza resultar em vazio (ex: o título era só "Chapter 1"), 
            # paramos para não perder a informação.
            if not novo_titulo:
                break
            titulo_limpo = novo_titulo
            
        # 3. Remove caracteres residuais que sobraram no início (como ":" ou "-")
        titulo_limpo = re.sub(r"^[偏\s:-]+", "", titulo_limpo)
        
        return titulo_limpo

    # Função para formatar o conteúdo como XHTML e converter para bytes
    def format_as_xhtml(self, content_list):
        parts = []

        for paragraph in content_list:
            text = paragraph.text
            escaped = (
                text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )
            parts.append(f"<p>{escaped}</p>")
        # Converte o conteúdo XHTML para bytes
        return "\n".join(parts).encode("utf-8")

    def runChapter(self, cap):
        time.sleep(0.55)
        response = self.session.get(self.url, headers=self.headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # container do capítulo
        match list(self.fonte.getConteudo().keys())[0]:
            case "class":
                contentElement = soup.find("div", class_=list(self.fonte.getConteudo().values())[0])
            case "id":
                contentElement = soup.find("div", id=list(self.fonte.getConteudo().values())[0])
            case _:
                raise ValueError("Tipo de busca para conteúdo do capítulo não suportado")

        if contentElement is None:
            raise ValueError("Conteúdo do capítulo não encontrado")

        # título
        match list(self.fonte.getTitulo().keys())[0]:
            case "class":
                tituloElement = soup.find(class_=list(self.fonte.getTitulo().values())[0])
            case "id":
                tituloElement = soup.find(id=list(self.fonte.getTitulo().values())[0])
            case "tag":
                tituloElement = contentElement.find(list(self.fonte.getTitulo().values())[0])
            case _:
                raise ValueError("Tipo de busca para título do capítulo não suportado")
        # if self.fonte.class_titulo:
        #     tituloElement = soup.find(class_=self.fonte.class_titulo)
        # else:
        #     tituloElement = contentElement.find(self.fonte.tag_titulo)

        if tituloElement is None:
            titulo = f"Chapter {cap}"
        else:
            titulo_real = self.getTitulo(tituloElement.get_text())
            
            # Se o título real for vazio ou apenas um número, usamos o padrão básico
            if not titulo_real or titulo_real.isdigit():
                titulo = f"Chapter {cap}"
            else:
                # Padronização final: Sempre "Chapter X: Título"
                titulo = f"Chapter {cap}: {titulo_real}"

        # conteúdo
        conteudo = contentElement.find_all(self.fonte.tag_conteudo)
        texto_xhtml = self.format_as_xhtml(conteudo)

        return Capitulo(titulo, texto_xhtml, cap, self.url)

    def updateNextButton(self):
        pass

    def atualizaUrl(self):
        if self.fonte.url_padrao:
            self.getNextUrlPadrao()
        # else:
        #     self.url = self.fonte.next_button.get_attribute('href')

    def getNextUrlPadrao(self):
        match = re.search(r"chapter-(\d+)", self.url)

        if not match:
            raise ValueError("Não foi possível identificar o número do capítulo na URL")

        capitulo_atual = int(match.group(1))
        proximo_capitulo = capitulo_atual + 1

        self.url = self.url.replace(
            f"chapter-{capitulo_atual}", f"chapter-{proximo_capitulo}"
        )
