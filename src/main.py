import logging
import sys
# Configure the root logger to output to stdout
logging.basicConfig(
  filename='myapp.log',
  format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
  datefmt='%d-%b-%y %H:%M:%S',
  level=logging.INFO,
  handlers=[logging.StreamHandler(sys.stdout)] # Directs logs to stdout
)

from application.pynovel_application import PyNovelApplication
from controller.pynovel_controller import PyNovelController as PyNovel
from controller.coletar_dados_controller import ColetarDadosController as ColetarDados
logger = logging.getLogger(__name__)

def main():
  logger.info('Started')
  app = PyNovelApplication(
    coletar_dados_controller= ColetarDados(),
    pynovel_controller= PyNovel
  )
  app.run()
  logger.info('Finished')

if __name__ == "__main__":
  main()
