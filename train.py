# -*- coding: utf-8 -*-

import os
from colorama import Fore

class Treino(object):

    idiomas_diponiveis = [
        "Inglês",
        "Russo",
        "Francês",
        "Polonês"
    ]

    idioma_selecionado = None
    livro_selecionado = None

    def __init__(self, books_db, translator):
        self.db = books_db
        self.translator = translator

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

    def _escolha_o_livro(self):
        print(Fore.LIGHTGREEN_EX + "\n### Escolha o livro" + Fore.RESET)
        books = self.db.all()

        while True:
            for i, c in enumerate(books):
                num = i+1
                print(Fore.LIGHTYELLOW_EX + str(num) + " - " + c["Title"] + Fore.RESET)


            e_livro = input("Escolha o livro (Vazio para cancelar)[%s - %s]: " % (1, len(books))).lower()

            if not e_livro:
                return False

            if e_livro == "n":
                pagina += 1
                continue

            try:
                self.livro_selecionado = books[int(e_livro) - 1]
                print("Livro selecionado: " + Fore.LIGHTYELLOW_EX + self.livro_selecionado["Title"] + Fore.RESET)
                return True
            except:
                print(Fore.RED + "Opção inválida!" + Fore.RESET)
                continue
    
    def _confirm(self):
        print(Fore.LIGHTGREEN_EX + "Confirme suas escolhas:" + Fore.RESET)
        print("Idioma: " + Fore.LIGHTYELLOW_EX + self.idioma_selecionado + Fore.RESET)
        print("Livro: " + Fore.LIGHTYELLOW_EX + self.livro_selecionado["Title"] + Fore.RESET)

        result = input("Confirma? (Y/n)").lower()

        if result == "n":
            return False
        
        return True

    def _iniciar_treino(self):
        titulo = self.livro_selecionado["Title"] 

        def limpar():
            cmd = "cls" if os.name == "nt" else "clear"
            os.system(cmd)

        def help():
            limpar()
            p_cmd("Seletores: ", [("p", "Parágrafo"), ("l","Linha"), ("w", "Palavra")])
            p_cmd("Modificadores: ", [("a", "Anterior"), ("n","Próximo")])
            print()
            print(Fore.LIGHTGREEN_EX + "Exemplos: " + Fore.RESET)
            print(Fore.GREEN + "np" + Fore.RESET + " - Vai para o próximo parágrafo")
            print(Fore.GREEN + "nl" + Fore.RESET + " - Vai para a próxima linha")
            print(Fore.GREEN + "3wa" + Fore.RESET + " - Volta 3 palavras")
            print(Fore.GREEN + "20np" + Fore.RESET + " - Avança 20 parágrafos")
            print()
            print("Pressione " + Fore.LIGHTYELLOW_EX + "<enter>" + Fore.RESET + " para sair") 
            input()
            

        def p_cmd(tipo, comandos, cor=Fore.LIGHTYELLOW_EX):
            print(Fore.LIGHTCYAN_EX + tipo + Fore.RESET + ", ".join("{}[{}] {}{}".format(cor, c[0], Fore.RESET, c[1]) for c in comandos))

        def mostrar(texto):
            limpar()
            print(Fore.LIGHTGREEN_EX + "{pad} {t} {pad}".format(pad="#" * 7, t=titulo) + Fore.RESET)
            print(Fore.BLUE + "\n### Original\n" + Fore.RESET)
            print(texto)
            print(Fore.BLUE + "\n### Tradução\n" + Fore.RESET)
            print(Fore.LIGHTWHITE_EX + str(self.translator.translate(texto, self.idioma_selecionado)) + Fore.RESET)

        while True:
            mostrar("Texto")
            print("\n" * 2)
            print(Fore.BLUE + "Digite -h para ajuda") 
            print("Comando: " + Fore.RESET, end="") 
            cmd = input()
            if cmd == "-h":
                help()

    def iniciar(self):
        print("\n" + Fore.LIGHTGREEN_EX + "### Treinando idioma\n" + Fore.RESET)
        
        if not self._escolha_o_idioma():
            return
        
        if not self._escolha_o_livro():
            return
        
        if not self._confirm():
            return
        
        self._iniciar_treino()


