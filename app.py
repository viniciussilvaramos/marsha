from pprint import pprint as p
from reader.epub import Epub
from translator import Translator

if __name__ == '__main__':
    e = Epub("/home/vvv/Downloads/O Exterminador do Futuro - James Cameron.epub")
    e.extract()
    #t = Translator()
    #p(t.translate("Gostaria que fallot 4 fosse tão maduro e cativante quanto Metro 2033", "russo"))
    #p(t.translate("Eu amei essa idéia!"))
    #p(t.translate("Eu amei essa idéia!", "francês"))
    #t.close()
