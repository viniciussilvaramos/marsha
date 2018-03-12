# -*- coding: utf-8 -*-

import sys, signal
from json import loads
from colorama import Fore, init
from db.books import BooksDB
from translation.bootstrap import Treino
from extractors.noticias import Source    

with open("config.json") as f:
    configs = loads(f.read())
    b = BooksDB(configs["db_uri"])
    debug = bool(configs["debug"])

s = Source()
t = Treino(s)

def sair(signal=None,frame=None):
    print(Fore.LIGHTGREEN_EX + "\n### Fui!" + Fore.RESET)
    sys.exit(0)

signal.signal(signal.SIGINT, sair)

def main():
    init()
    opcoes = [
        "Treinar",
        "Sair",
    ]

    while True:
        print("\n" + Fore.LIGHTGREEN_EX + "### Home" + Fore.RESET)
        print("Escolha o que você deseja fazer:")
        for i, opcao in enumerate(opcoes):
            print( "%s[%s]%s - %s" % (Fore.LIGHTYELLOW_EX, i+1, Fore.RESET, opcao))

        answer = input("Escolha: ")

        if answer == "2":
           sair() 
        elif answer == "1":
            t.iniciar()
        else:
            print(Fore.LIGHTRED_EX + "Escolha inválida!" + Fore.RESET)

if __name__ == '__main__':
    if debug:
        main()
    else:
        try:
            main()
        finally:    
            sair()
