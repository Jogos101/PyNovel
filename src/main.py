from application.PyNovelApplication import PyNovelApplication
from controller.PyNovelController import PyNovelController as PyNovel
from controller.ColetarDadosController import ColetarDadosController as ColetarDados
from factory.WebScraperFactory import WebScraperFactory
from services import EpubService

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
