# -*- coding: utf-8 -*-

import sys, signal
from json import loads
from colorama import Fore, init
from db.books import BooksDB
from translation.bootstrap import Treino
from extractors.gutenberg import Gutenberg

with open("config.json") as f:
    b = BooksDB(loads(f.read())["db_uri"])

t = Treino(b)

def baixar_livros():
    print("\n" + Fore.LIGHTGREEN_EX + "### Baixando livros" + Fore.RESET)
    g = Gutenberg(b)
    g.start()
    print(Fore.GREEN + "### Voltando para opções iniciais.\n" + Fore.RESET)

def sair(signal=None,frame=None):
    print(Fore.LIGHTGREEN_EX + "\n### Fui!" + Fore.RESET)
    sys.exit(0)

signal.signal(signal.SIGINT, sair)

def main():
    init()
    while True:
        print("\n" + Fore.LIGHTGREEN_EX + "### Home" + Fore.RESET)
        print("Escolha o que você deseja fazer:")
        print(Fore.LIGHTYELLOW_EX + "[B]" + Fore.RESET + "aixar os livros de domínio público do Gutenberg.org;")
        print(Fore.LIGHTYELLOW_EX + "[T]" + Fore.RESET + "reinar algum idioma;")
        print(Fore.LIGHTYELLOW_EX + "[S]" + Fore.RESET + "air;")
        answer = input("Escolha: [B, T, S]: ").lower()

        if answer == "s":
           sair() 

        if answer == "b":
            baixar_livros()

        elif answer == "t":
            t.iniciar()

        else:
            print(Fore.LIGHTRED_EX + "Escolha inválida!" + Fore.RESET)

if __name__ == '__main__':
    #try:
        #main()
    #finally:    
        #sair()
    main()
