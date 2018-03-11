import os
from json import loads
from db.books import BooksDB
from translation.interface import UserInterface
from translation.common import Navigator, Command
from time import sleep

with open(os.path.join(os.path.dirname(__file__), "config.json"))  as f:
    b = BooksDB(loads(f.read())["db_uri"])

livro = b.all()[1]
paragrafos = b.content(livro["Id"])["Content"]

#for p in paragrafos:
#    print(p)
#    sleep(3)

#n = Navigator(paragrafos)
#print(n.get(Command("10n")))
#print(n.get(Command("10n")))
#print(n.get(Command("10n"))) 
ui = UserInterface("francês", livro, paragrafos)
ui.iniciar_treino()
