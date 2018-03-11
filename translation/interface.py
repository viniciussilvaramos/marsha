import os
import sys, signal
from colorama import Fore
from engine.brownser import Translator
from .common import limpar, help, Command, Navigator

class UserInterface(object):

    def __init__(self, idioma, livro, paragrafos):
        self.tr = Translator()
        self.idioma = idioma
        self.livro = livro
        self.nav = Navigator(paragrafos)
        signal.signal(signal.SIGINT, lambda x,y: self.tr.close())

    def mostrar(self, texto, meta):
        limpar()
        titulo = self.livro["Title"] 
        print(Fore.LIGHTGREEN_EX + "{pad} {t} {pad}".format(pad="#" * 7, t=titulo) + Fore.RESET)
        for m in meta:
            print(Fore.BLUE + "{}: {}".format(m, meta[m]) + Fore.RESET)
        print(Fore.BLUE + "\n### Original\n" + Fore.RESET)
        print(texto)
        print(Fore.BLUE + "\n### Tradução\n" + Fore.RESET)
        
        result = self.tr.translate(texto, self.idioma)

        print(result["latin"])
        if "ideogram"in result:
            print()
            print(Fore.YELLOW + "Ideograma: " + Fore.RESET + result["ideogram"])

    def obter_proximo(self, cmd):
        command = Command(cmd)
        text = self.nav.get(command)
        return text

    def iniciar_treino(self):
        cmd = "10n"
        meta = {}
        try:
            while True:
                meta["Ultimo Comando"] = cmd 
                texto = self.obter_proximo(cmd)
                self.mostrar(texto, meta)
                meta["Ultima Frase"] = texto 
                print("\n")
                print(Fore.BLUE + "Digite -h para ajuda") 
                print("Comando: " + Fore.RESET, end="") 
                u_cmd = input()
                if u_cmd == "-h":
                    help()
                elif u_cmd == "-s" or u_cmd == "s" or u_cmd == "q":
                    self.tr.close()
                    return
                elif u_cmd == "":    
                    continue

                cmd = u_cmd
        finally:
            self.tr.close()
