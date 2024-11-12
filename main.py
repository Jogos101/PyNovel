# Importando as bibliotecas necessárias
# import pandas as pd
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
from tqdm import tqdm
# import time
import re
import pypub

"""# Parâmetros"""

# Configurações do Chrome no modo headless (sem interface gráfica)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Dados do livro
titulo_livro = "I Am The Fated Villain"
autor = "Fated Villain"
idioma = "en"
arquivo = "./livros/I-am-the-fated-villain"

# Url sem o padrão de capítulos
url_inicial = "https://novelbin.lanovels.net/book/i-am-the-fated-villain/chapter-1-young-lord-gu-changge?subsite=1"

# Quantidade de capítulos
total_capitulos = 972

# Dados HTML
class_titulo = "chr-text"
class_conteudo = "chr-content"
next_chap = "next_chap"
next_disabled = "disabled"
tag_conteudo = "p"

"""# Funções"""

# Função de limpeza do título
def getTitulo(elemento):
  # Expressão regular para remover 'Chapter' e os números que seguem (opcionalmente com ':')
  refined_title = re.sub(r'Chapter \d+(:|\s)?', '', elemento).strip()
  # Retorna o título limpo
  return refined_title

# Função para formatar o conteúdo como XHTML e converter para bytes
def format_as_xhtml(content_list):
  formatted_content = ''
  for paragraph in content_list:
    # Escape special characters in paragraph text
    escaped_text = paragraph.text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    formatted_content += f'<p>{escaped_text}</p>\n'
  # Limpa o conteúdo XHTML com BeautifulSoup
  # soup = BeautifulSoup(formatted_content, 'html.parser')
  # Converte o conteúdo XHTML para bytes
  return formatted_content.encode('utf-8')

"""# Web Scraping"""

# Inicializa o WebDriver
driver = webdriver.Chrome(options=options)

# Cria o e-pub com título, autor e idioma
epub = pypub.Epub(titulo_livro, autor, idioma)

# Define a URL inicial (primeiro capítulo)
url = url_inicial

# Para cada capítulo
with tqdm(total=total_capitulos, desc="Processando", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} | Percorrido: {elapsed} | Restante: {remaining}") as pbar:
    for cap in range(1, total_capitulos + 1):
      try:
        # Jogar o conteúdo do URL no WebDriver
        driver.get(f"{url}")

        # Selecionar o elemento do título
        tituloElement = driver.find_element(By.CLASS_NAME, class_titulo) # By.ID ou By.CLASS_NAME
        # Pegar o título
        titulo_limpo = getTitulo(tituloElement.text)
        if titulo_limpo.find(":") == -1:
          titulo = f'Chapter {cap}: ' + titulo_limpo
        else:
          titulo = titulo_limpo

        # Selecionar o conteúdo
        contentElement = driver.find_element(By.ID, class_conteudo) # By.ID ou By.CLASS_NAME
        # Pegar o conteúdo inteiro
        conteudo = contentElement.find_elements(By.TAG_NAME, tag_conteudo)

        # Formata o conteúdo como XHTML
        texto_xhtml = format_as_xhtml(conteudo)

        # Cria o capítulo com conteúdo e título
        capitulo = pypub.Chapter(content=texto_xhtml, title=titulo, url=url)
        epub.add_chapter(capitulo)

        # Registro
        # tqdm.write(f'[{titulo}] concluído')

        # Atualizar a barra de progresso
        pbar.update(1)
        pbar.refresh()

        # Seleciona o botão de próximo capítulo
        next_button = driver.find_element(By.ID, next_chap) # By.ID ou By.CLASS_NAME

        # Verifica se o próximo botão está desativado
        if next_disabled in next_button.get_attribute('class') or next_button.get_attribute('disabled'):
          print("Botão de próximo capítulo está desativado. Finalizando a coleta de capítulos.")
          pbar.n = pbar.total  # Força o progresso a 100%
          pbar.refresh()
          break  # Sai do loop se o botão está desativado

        # Atualiza a URL para o próximo capítulo
        url = next_button.get_attribute('href')
      except Exception as e:
            print(f"Erro ao processar o capítulo {cap}: {e}")
            pbar.n = pbar.total  # Força o progresso a 100%
            pbar.refresh()
            break

# Gera o arquivo epub
epub.create(arquivo)

# Fecha o driver ao final do processo
driver.quit()