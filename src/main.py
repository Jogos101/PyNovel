from controller.PyNovelController import PyNovelController as PyNovel
from controller.ColetarDadosController import ColetarDadosController as ColetarDados

if __name__ == "__main__":
  PyNovel(*ColetarDados().coletar())
