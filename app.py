# -*- coding: utf-8 -*-

from translator.selenium import Translator
from db.books import BooksDB
from helper.gutenberg import Gutenberg
from colorama import Fore, init
from json import loads
from train import Treino

with open("config.json") as f:
    b = BooksDB(loads(f.read())["db_uri"])

t = Treino(b)

def baixar_livros():
    print("\n" + Fore.LIGHTGREEN_EX + "### Baixando livros" + Fore.RESET)
    g = Gutenberg(b)
    g.start()
    print(Fore.GREEN + "### Voltando para opções iniciais.\n" + Fore.RESET)

def main():
    init()
    while True:
        print("\n" + Fore.LIGHTGREEN_EX + "### Home" + Fore.RESET)
        print("Escolha o que você deseja fazer:")
        print(Fore.LIGHTYELLOW_EX + "[B]" + Fore.RESET + "aixar os livros de domínio público do Gutenberg.org;")
        print(Fore.LIGHTYELLOW_EX + "[T]" + Fore.RESET + "reinar algum idioma")
        answer = input("Escolha: [B, T]: ").lower()

        if answer == "b":
            baixar_livros()

        elif answer == "t":
            t.iniciar()

        else:
            print(Fore.LIGHTRED_EX + "Escolha inválida!" + Fore.RESET)

if __name__ == '__main__':
    main()
