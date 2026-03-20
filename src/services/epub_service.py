from abc import ABC, abstractmethod

import pypub # type: ignore
import src.entity.livro
import src.entity.capitulo 
from pathlib import Path

class EpubService(ABC):
    @abstractmethod
    def criar_capitulo(self, capitulo):
        pass

    @abstractmethod
    def gerar_epub(self):
        pass

    @abstractmethod
    def set_arquivo(self):
        pass
    
    @abstractmethod
    def controlar_concorrencia(self, output_dir):
        pass