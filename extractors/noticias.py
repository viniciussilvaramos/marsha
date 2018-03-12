import requests
from pprint import pprint as p
from bs4 import BeautifulSoup

class Noticia(object):
    
    def __init__(self, el):
        self.Titulo = el.title.getText()
        self.Descricao = el.description.getText()
        self.Link = el.link.getText()
        self._content = None

    @property
    def Content(self):
        if not self._content:
            response = requests.get(self.Link)
            response.encoding = 'utf-8'
            text = response.text

            bs = BeautifulSoup(text, "lxml")
            for tag in bs(['style', 'script']):
                tag.extract()

            content = []
            for el in bs.body.findAll('p'):
                t = el.get_text().strip()
                if t:
                    content.append(t)
            self._content = content

        return self._content


class Source(object):
    fontes = [
        "http://rss.home.uol.com.br/index.xml",
    #     "http://rss.uol.com.br/feed/noticias.xml"
    #     "http://tecnologia.uol.com.br/ultnot/index.xml",
    #     "http://esporte.uol.com.br/futebol/ultimas/index.xml",
    #     "http://rss.uol.com.br/feed/jogos.xml",
    #     "http://musica.uol.com.br/ultnot/index.xml",
    #     "http://rss.carros.uol.com.br/ultnot/index.xml",
    #     "http://cinema.uol.com.br/ultnot/index.xml",
    #     "http://rss.uol.com.br/feed/economia.xml",
    ]

    def __init__(self):
        self._noticias = []
    
    @property
    def noticias(self):
        if not self._noticias:
            for fonte in self.fontes:
                response = requests.get(fonte)
                response.encoding = 'utf-8' 
                text = response.text

                bs = BeautifulSoup(text, "lxml-xml")
                for el in bs.findAll("item"):
                    self._noticias.append(Noticia(el))
        
        return self._noticias

if __name__ == '__main__':
    n = Noticias()
    noticia = n.noticias[0]
    p(noticia.Content)