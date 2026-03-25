from application.pynovel_application import PyNovelApplication
from controller.pynovel_controller import PyNovelController as PyNovel
from controller.coletar_dados_controller import ColetarDadosController as ColetarDados

def main():
  app = PyNovelApplication(
    coletar_dados_controller= ColetarDados(),
    pynovel_controller= PyNovel
  )
  app.run()

if __name__ == "__main__":
  main()
