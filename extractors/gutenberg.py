import os
import requests
from colorama import init, Fore
from bs4 import BeautifulSoup
from parsel import Selector
from time import sleep
from threading import Thread

class Gutenberg(object):

    def __init__(self, book_db):
        init()
        self.book_db = book_db
        self.extracted = []
        self.status = None

    def _has_lockfile(self):
        return os.path.exists("gutenberg.lock")

    def start_async(self):
        if self._has_lockfile():
            return self.status

        self._create_lock()

        t = Thread(target=self._save)
        t.start()
    
    def start(self):
        self._save()

    def get_extracted(self):
        return self.extracted

    def _create_lock(self):
        with open("gutenberg.lock", "w") as f:
            f.write("Begin!");
    
    def _save(self):
        for b in self._get_books():
            book, paragraphs = b
            self.book_db.save(book, paragraphs)
            self.extracted.append(book["Title"])
            print("# Baixado: " + Fore.LIGHTYELLOW_EX + book["Title"] + Fore.RESET)
        
        if self._has_lockfile():
            os.remove("gutenberg.lock")

        self.status = "DONE"

    def _get_books(self):
        self.status = "RUNNING"
        top100 = self._get_top_100()
        for i, book in enumerate(top100):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
                ,'Referer':	'http://www.gutenberg.org/ebooks/%s' % book["GutenbergId"]
            }
            response = requests.get("http://www.gutenberg.org/files/{id}/{id}-h/{id}-h.htm".format(id=book["GutenbergId"]), headers=headers)
            response.encoding = "utf-8"

            book["Rank"] = i+1
            book.pop("GutenbergId",None)

            paragraphs = list(self._separate(response.text))

            sleep(1)
            yield (book, paragraphs)


    def _get_top_100(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
        url = "http://www.gutenberg.org/browse/scores/top" 
        response = requests.get(url, headers=headers)
        se = Selector(response.text)
        books = []
        for item in se.xpath("//h2[@id='books-last1']/following-sibling::ol[1]/li"):
            href = item.xpath("./a/@href").extract_first()
            id = href.split("/")[-1]
            books.append({
                "Title": item.xpath("./a/text()").extract_first(),
                "Url": "http://www.gutenberg.org" + href,
                "GutenbergId": id
            })
        return books

    def _separate(self, text):
        bs = BeautifulSoup(text, "lxml")
        for el in bs.body:
            if hasattr(el, "text"):
                value = el.text.strip()
                if value:
                    yield value

if __name__ == '__main__':
    from db.books import BooksDB
    g = Gutenberg(BooksDB("sqlite:///books.db"))
    g.start()
