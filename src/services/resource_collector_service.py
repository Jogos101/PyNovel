import json
from src.services.file_path_service import FilePathService

class ResourceCollectorService:
    def __init__(self):
        self.file_path_service = FilePathService()

    def listar_fontes(self):
        return self.file_path_service.get_all_sources()

    def get_dados_livro(self, fonte_selecionada):
        # Carregar os dados do livro a partir do arquivo JSON
        fonte_path = self.file_path_service.get_source_path(fonte_selecionada)

        with open(fonte_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        cover = None
        try:
            cover_path = self.file_path_service.get_cover_path(fonte_selecionada)
            cover = str(cover_path)
        except FileNotFoundError:
            pass

        return (data["Name"], data["autor"], data.get("idioma", "en"), cover)
    
    def get_dados_fonte(self, fonte_selecionada):
        # Carregar os dados da fonte a partir do arquivo JSON
        fonte_path = self.file_path_service.get_source_path(fonte_selecionada)

        with open(fonte_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return (data["url_inicial"], data["url_padrao"], data["total_capitulos"], data["titulo"], data["conteudo"], data["next_chap"], data["next_disabled"], data["tag_conteudo"])