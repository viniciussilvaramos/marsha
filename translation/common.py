from colorama import Fore

def limpar():
    cmd = "cls" if os.name == "nt" else "clear"
    os.system(cmd)

def p_cmd(tipo, comandos, cor=Fore.LIGHTYELLOW_EX):
    print(Fore.LIGHTCYAN_EX + tipo + Fore.RESET + ", ".join("{}[{}] {}{}".format(cor, c[0], Fore.RESET, c[1]) for c in comandos))


def help():
    limpar()
    p_cmd("Navegadores: ", [("a", "Anterior"), ("n","Próximo")])
    print()
    print(Fore.CYAN + "{quantidade}{navegador}" + Fore.RESET + " - Anvança/Retrocede o texto com base na quantidade e no navegador fornecido")
    print(Fore.LIGHTGREEN_EX + "Exemplos: " + Fore.RESET)
    print(Fore.GREEN + "10n" + Fore.RESET + " - Exibe as 10 próximas palavras")
    print(Fore.GREEN + "3a" + Fore.RESET + " - Exibe as 3 ultimas palavras")
    print()
    print(Fore.GREEN + "<enter>" + Fore.RESET + " - Repete o ultimo comando")
    print()
    print("Pressione " + Fore.LIGHTYELLOW_EX + "<enter>" + Fore.RESET + " para sair") 
    input()

class Command(object):
    def __init__(self, cmd):
        nav, qtd = self._parse_command(cmd)
        self.Navigator = nav 
        self.Quantidade = qtd

    def _parse_command(self, command):
        if not command:
            raise Exception("Comando inválido!")

        cmd = list(command[::-1])
        nav = cmd.pop(0)
        
        if nav not in ["n", "a"]:
            raise Exception("Comando inválido!")

        try:
            if len(cmd) > 0:
                qtd = int("".join(cmd[::-1]))
            else:
                qtd = 1
        except:
            raise Exception("Comando inválido!")

        return (nav, qtd)
    
    def get(self):
        nav = 1
        if self.Navigator == "a":
            nav = -1
        
        return nav * self.Quantidade
 
class Navigator(object):

    def __init__(self, array):
        if not array:
            raise Exception("Não há valores para navegar!")

        self.text = self._get_text(array)
        self.current_pos = 0

        self.end = False
        self.begin = False

    def _get_text(self, array):
        text = " ".join(array)
        return text.split()

    def _get_next(self, counter):
        fr = 0
        to = 0

        if counter < 0:
            fr = self.current_pos + counter
            to = self.current_pos
        else:
            fr = self.current_pos
            to = self.current_pos + counter

        #print(locals())

        if fr < 0:
            fr = 0
        if to > len(self.text):    
            to = len(self.text)

        if counter < 0:
            self.current_pos = fr
        else:
            self.current_pos = to

        #print(locals())
        return self.text[fr:to]
        #self.begin = False
        #self.end = False
#
        #if self.curr_pos < 0:
            #self.begin = True
            #self.curr_pos = 0
#
        #if self.curr_pos > len(self.text) - 1:
            #self.end = True
            #self.curr_pos = len(self.text) -1
#
        #return self.text[self.curr_pos]
        

    def get(self, command=None): 
        if command != None:
            return " ".join(self._get_next(command.get()))

        return " ".join(self._get_next(1))


if __name__ == '__main__':
    arr = [
            "É claro que a contínua expansão de nossa atividade desafia a capacidade de equalização de todos os recursos funcionais envolvidos.",
            "A nível organizacional, o desafiador cenário globalizado promove a alavancagem da gestão inovadora da qual fazemos parte.",
            "Caros amigos, o aumento do diálogo entre os diferentes setores produtivos assume importantes posições no estabelecimento das novas proposições."
    ] 
    #print(Command("10n").get())
    #print(Command("10a").get())
    print(Fore.CYAN + " ".join(arr) + Fore.RESET)
    print()
    n = Navigator(arr)
    print(n.get(Command("1110n")))
    print(n.get(Command("10a")))
    print(n.get(Command("10a")))
    print(n.get(Command("10a")))
    print(n.get(Command("10a")))
