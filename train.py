# -*- coding: utf-8 -*-

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

    def __init__(self, books_db):
        self.db = books_db

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
        pagina = 1

        while True:
            current = books[pagina-1:10]
            for i, c in enumerate(current):
                print(Fore.LIGHTYELLOW_EX + str(i + 1) + " - " + c["Title"] + Fore.RESET)

            e_livro = input("Escolha o livro [%s - %s, N para próxima página]: " % (pagina, pagina*10)).lower()

            if not e_livro:
                return False

            if e_livro == "n":
                pagina += 1
                continue

            try:
                self.livro_selecionado = current[int(e_livro) - 1]
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

    def iniciar(self):
        print("\n" + Fore.LIGHTGREEN_EX + "### Treinando idioma\n" + Fore.RESET)
        
        if not self._escolha_o_idioma():
            return
        
        if not self._escolha_o_livro():
            return
        
        if not self._confirm():
            return



