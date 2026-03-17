from pathlib import Path
import json

class ResourceCollectorService:
    def __init__(self):
        pass

    def listar_fontes(self):
        # Listar as fontes disponíveis
        base_path = Path(__file__).resolve().parent.parent.parent
        fontes_dir = base_path / "resources" / "sources"

        # Cria o diretório de saída se ele não existir
        fontes_dir.mkdir(parents=True, exist_ok=True)

        fontes = [f.stem for f in fontes_dir.glob("*.json") if f.stem != 'exemplo_source']
        return fontes

    def get_dados_livro(self, fonte_selecionada):
        # Carregar os dados do livro a partir do arquivo JSON
        base_path = Path(__file__).resolve().parent.parent.parent
        fonte_path = base_path / "resources" / "sources" / f"{fonte_selecionada}.json"

        with open(fonte_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        cover_path = base_path / "resources" / "covers" / f"{fonte_selecionada}.jpg"
        cover = None
        if cover_path.exists():
            cover = str(cover_path)

        return (data["Name"], data["autor"], data.get("idioma", "en"), cover)
    
    def get_dados_fonte(self, fonte_selecionada):
        # Carregar os dados da fonte a partir do arquivo JSON
        base_path = Path(__file__).resolve().parent.parent.parent
        fonte_path = base_path / "resources" / "sources" / f"{fonte_selecionada}.json"

        with open(fonte_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return (data["url_inicial"], data["url_padrao"], data["total_capitulos"], data["titulo"], data["conteudo"], data["next_chap"], data["next_disabled"], data["tag_conteudo"])