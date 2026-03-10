from entity.Fonte import Fonte
from entity.Capitulo import Capitulo
from factory.FindElementFactory import FindElementFactory

# import pandas as pd
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import time
import re

class WebScrapingService:
    def __init__(self, fonte):
        self.fonte = fonte
        self.url = fonte.url_inicial
        self.driver = self.iniciarWebScrapping()
        self.wait = WebDriverWait(self.driver, 10)
        self.chapter_regex = re.compile(r'Chapter \d+(:|\s)?')

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
        # Limpa o conteúdo XHTML com BeautifulSoup
        # soup = BeautifulSoup(formatted_content, 'html.parser')
        # Converte o conteúdo XHTML para bytes
        return "\n".join(parts).encode("utf-8")
    
    def runChapter(self, cap):
        # Jogar o conteúdo do URL no WebDriver
        self.driver.get(f"{self.url}")

        # Selecionar o conteúdo
        contentElement = self.driver.find_element(By.CLASS_NAME, self.fonte.class_conteudo) # By.ID ou By.CLASS_NAME

        # Selecionar o elemento do título
        if self.fonte.class_titulo != None:
            tituloElement = contentElement.find_element(By.CLASS_NAME, self.fonte.class_titulo) # By.ID ou By.CLASS_NAME
        else:
            tituloElement = contentElement.find_element(By.TAG_NAME, self.fonte.tag_titulo)

        # Pegar o título
        titulo_limpo = self.getTitulo(tituloElement.text)

        if ":" not in titulo_limpo:
            titulo = f"Chapter {cap}: {titulo_limpo}"
        else:
            titulo = titulo_limpo

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