# -*- coding: utf-8 -*-

import os
from colorama import Fore
from .interface import UserInterface

class Treino(object):

    idiomas_diponiveis = [
        "Inglês",
        "Russo",
        "Francês",
        "Polonês"
    ]

    idioma_selecionado = None

    def __init__(self, noticias):
        self.noticias = noticias

    def _escolha_o_idioma(self):
        print(Fore.LIGHTGREEN_EX + "\n### Escolha o idioma" + Fore.RESET)
        print("Idiomas Disponíveis:")
        while True:
            for index, idioma in enumerate(self.idiomas_diponiveis):
                print(Fore.LIGHTYELLOW_EX + str(index + 1) + Fore.RESET + " - " + idioma)
            
            e_idioma = input("Qual idioma (Deixe vazio para cancelar) [%s]: " % ",".join((str(i+1) for i in range(len(self.idiomas_diponiveis)))))

            if not e_idioma:
                return 
            
            try:
                self.idioma_selecionado = self.idiomas_diponiveis[int(e_idioma) - 1]
                print("Idioma selecionado: " + Fore.LIGHTYELLOW_EX + self.idioma_selecionado + Fore.RESET)
                return True
            except:
                print(Fore.RED + "Opção inválida!" + Fore.RESET)
                continue

    def _confirm(self):
        print(Fore.LIGHTGREEN_EX + "Confirme suas escolhas:" + Fore.RESET)
        print("Idioma: " + Fore.LIGHTYELLOW_EX + self.idioma_selecionado + Fore.RESET)

        result = input("Confirma? (Y/n)").lower()

        if result == "n":
            return False
        
        return True

    def iniciar(self):
        print("\n" + Fore.LIGHTGREEN_EX + "### Treinando idioma\n" + Fore.RESET)
        
        if not self._escolha_o_idioma():
            return
        
        if not self._confirm():
            return

        for noticia in self.noticias.noticias:
            ui = UserInterface(self.idioma_selecionado, noticia, noticia.Content)
            ui.iniciar_treino()


