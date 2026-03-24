from src.services.epub_service import EpubService
from factory.web_scraper_factory import WebScraperFactory
from application.pynovel_application import PyNovelApplication
from controller.pynovel_controller import PyNovelController as PyNovel
from controller.coletar_dados_controller import ColetarDadosController as ColetarDados

def main():
  app = PyNovelApplication(
    coletar_dados_controller= ColetarDados(),
    webscraper_factory= WebScraperFactory,
    epub_service= EpubService,
    pynovel_controller= PyNovel
  )
  app.run()

if __name__ == "__main__":
  main()
