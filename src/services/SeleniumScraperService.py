from entity.Fonte import Fonte
from entity.Capitulo import Capitulo
from factory.FindElementFactory import FindElementFactory
from services.WebScrapingInterface import WebScrapingInterface
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import time
import re

class SeleniumScraperService(WebScrapingInterface):
    def __init__(self, fonte: Fonte):
        self.fonte = fonte
        self.url = fonte.url_inicial
        self.driver = self.iniciarWebScrapping()
        self.wait = WebDriverWait(self.driver, 10)

    def iniciarWebScrapping(self):
        # Configurações do Chrome no modo headless (sem interface gráfica)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-images")
        options.add_argument("--blink-settings=imagesEnabled=false")
        # Inicializa o WebDriver
        return webdriver.Chrome(options=options)

    # Função de limpeza do título
    def getTitulo(self, elemento):
        # 1. Regex que captura: "Chapter", espaço, números (ou intervalos como 20-18) 
        # e qualquer combinação de ": ", " - " ou espaços que venham depois.
        # A flag re.IGNORECASE garante que pegue 'chapter' ou 'Chapter'.
        pattern = re.compile(r"Chapter\s+\d+(\s*-\s*\d+)?[:\s-]*", re.IGNORECASE)
        
        titulo_limpo = elemento.text.strip()
        
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
                text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
            )
            parts.append(f"<p>{escaped}</p>")
        # Converte o conteúdo XHTML para bytes
        return "\n".join(parts).encode("utf-8")
    
    def runChapter(self, cap):
        # Jogar o conteúdo do URL no WebDriver
        self.driver.get(f"{self.url}")

        # container do capítulo
        match list(self.fonte.getConteudo().keys())[0]:
            case "id":
                # Selecionar o conteúdo
                contentElement = self.driver.find_element(By.ID, list(self.fonte.getConteudo().values())[0]) # By.ID ou By.CLASS_NAME
            case "class":
                # Selecionar o conteúdo
                contentElement = self.driver.find_element(By.CLASS_NAME, list(self.fonte.getConteudo().values())[0]) # By.ID ou By.CLASS_NAME
            case _:
                raise ValueError("Tipo de busca para conteúdo do capítulo não suportado")

        if contentElement is None:
            raise ValueError("Conteúdo do capítulo não encontrado")
        
        # título
        match list(self.fonte.getTitulo().keys())[0]:
            case "class":
                titulo_elements = self.driver.find_elements(By.CLASS_NAME, list(self.fonte.getTitulo().values())[0])
                if titulo_elements:
                    tituloElement = titulo_elements[0]
                else:
                    tituloElement = None
            case "id":
                titulo_elements = self.driver.find_elements(By.ID, list(self.fonte.getTitulo().values())[0])
                if titulo_elements:
                    tituloElement = titulo_elements[0]
                else:
                    tituloElement = None
            case _:
                raise ValueError("Tipo de busca para título do capítulo não suportado")

        if tituloElement is None:
            titulo = f"Chapter {cap}"
        else:
            titulo_real = self.getTitulo(tituloElement)
            
            # Se o título real for vazio ou apenas um número, usamos o padrão básico
            if not titulo_real or titulo_real.isdigit():
                titulo = f"Chapter {cap}"
            else:
                # Padronização final: Sempre "Chapter X: Título"
                titulo = f"Chapter {cap}: {titulo_real}"

        # Pegar o conteúdo inteiro
        conteudo = contentElement.find_elements(By.TAG_NAME, self.fonte.tag_conteudo)
        # Formata o conteúdo como XHTML
        texto_xhtml = self.format_as_xhtml(conteudo)

        return Capitulo(titulo, texto_xhtml, cap, self.url)

    def updateNextButton(self):
        self.fonte.next_button = self.driver.find_element(By.ID, self.fonte.next_chap) # By.ID ou By.CLASS_NAME
        if self.next_disabled in self.fonte.next_button.get_attribute('class') or self.fonte.next_button.get_attribute('disabled'):
            return False
        else:
            return True
        
    def atualizaUrl(self):
        if self.fonte.url_padrao:
            self.getNextUrlPadrao()
        else:
            self.url = self.fonte.next_button.get_attribute('href')

    def getNextUrlPadrao(self):
        match = re.search(r'chapter-(\d+)', self.url)

        if not match:
            raise ValueError("Não foi possível identificar o número do capítulo na URL")

        capitulo_atual = int(match.group(1))
        proximo_capitulo = capitulo_atual + 1

        self.url = self.url.replace(f"chapter-{capitulo_atual}", f"chapter-{proximo_capitulo}")

    def endScraping(self):
        # Fecha o driver ao final do processo
        self.driver.quit()