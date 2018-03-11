import os
import sys, signal
from colorama import Fore
from engine.brownser import Translator
from .common import limpar, help

class UserInterface(object):

    def __init__(self, idioma, livro, paragrafos):
        self.tr = Translator()
        self.idioma = idioma
        self.livro = livro
        self.paragrafos = paragrafos 
        signal.signal(signal.SIGINT, lambda x,y: self.tr.close())

    def mostrar(self, texto, meta):
        limpar()
        titulo = self.livro["Title"] 
        print(Fore.LIGHTGREEN_EX + "{pad} {t} {pad}".format(pad="#" * 7, t=titulo) + Fore.RESET)
        print(Fore.BLUE + "\n### Original\n" + Fore.RESET)
        print(texto)
        print(Fore.BLUE + "\n### Tradução\n" + Fore.RESET)
        
        result = self.tr.translate(texto, self.idioma)

        print(result["latin"])
        if "ideogram"in result:
            print()
            print(Fore.YELLOW + "Ideograma: " + Fore.RESET + result["ideogram"])

    def obter_proximo(self, command):
        if not command:
            raise Exception("Invalid command!")

        cmd = command[::-1]
        sel = cmd.pop(0)
        mod = cmd.pop(0)
        qtd = 1 
    

    def iniciar_treino(self):
        cmd = "p"
        try:
            while True:
                meta, texto = self.obter_proximo(cmd)
                self.mostrar(texto, meta)
                print("\n" * 2)
                print(Fore.BLUE + "Digite -h para ajuda") 
                print("Comando: " + Fore.RESET, end="") 
                cmd = input()
                if cmd == "-h":
                    help()
                elif cmd == "-s":
                    self.tr.close()
                    return
        finally:
            self.tr.close()
