from bs4 import BeautifulSoup
import requests
import os
from parsel import Selector
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model import Book, Paragraph

engine = create_engine('sqlite:///books.db')
DBSession = sessionmaker(bind=engine)

session = DBSession()

def get_books():
    top100 = _get_top_100()
    for i, book in enumerate(top100):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
            ,'Referer':	'http://www.gutenberg.org/ebooks/%s' % book["GutembergId"]
        }
        response = requests.get("http://www.gutenberg.org/files/{id}/{id}-h/{id}-h.htm".format(id=book["GutembergId"]), headers=headers)
        response.encoding = "utf-8"

        book["Rank"] = i+1

        b = Book(**book)
        session.add(b)

        for pl in separate(response.text):
            p = Paragraph(Value=pl, Book=b)
            session.add(p)
        
        session.commit()
        

        print("Saved: " + book["Title"])
        sleep(1)


def _get_top_100():
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
            "GutembergId": id
        })
    return books

def separate(text):
    bs = BeautifulSoup(text, "lxml")
    for el in bs.body:
        if hasattr(el, "text"):
            value = el.text.strip()
            if value:
                yield value

if __name__ == '__main__':
    get_books()
    print("Done")
