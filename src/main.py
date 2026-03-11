# pip install tqdm
# pip install pypub3
# pip install selenium
# pip install requests
# pip install beautifulsoup4

# Importando controller
from controller.PyNovelController import PyNovelController as PyNovel
from entity.Livro import Livro
from entity.Fonte import Fonte

# Dados do livro
titulo_livro = "Immortality Through Array Formations"
autor = "Observing the Emptiness, 观虚"
idioma = "en"

# Url sem o padrão de capítulos
url_inicial = "https://freewebnovel.com/novel/immortality-through-array-formations/chapter-1"
# Quantidade de capítulos
total_capitulos = 2181
# Dados HTML
class_titulo = None
tag_titulo = "h4"
class_conteudo = "txt"
id_conteudo = None
url_padrao = True
next_chap = "next_chap"
next_disabled = "disabled"
tag_conteudo = "p"

livro = Livro(titulo_livro, autor, idioma)
# url, url_padrao, total_capitulos, class_titulo, tag_titulo, class_conteudo, next_chap, next_end, tag_conteudo
fonte = Fonte(url_inicial, url_padrao, total_capitulos, class_titulo, tag_titulo, class_conteudo, next_chap, next_disabled, tag_conteudo)

PyNovel(fonte, livro).start()

# titulo = {
#     "id": None,
#     "class": None,
#     "tag": "h4"
# }
# conteudo = {
#     "id": None,
#     "class": "txt",
#     "tag": None
# }