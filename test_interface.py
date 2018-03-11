import os
from json import loads
from db.books import BooksDB
from translation.interface import UserInterface
with open(os.path.join(os.path.dirname(__file__), "config.json"))  as f:
    b = BooksDB(loads(f.read())["db_uri"])

livro = b.all()[0]
paragrafos = b.content(livro["Id"])
ui = UserInterface("francês", livro, paragrafos)
ui.iniciar_treino()
