from pprint import pprint as p
from reader.epub import Epub
from translator import Translator
from flask import Flask, render_template, jsonify
from db.model import Book, Paragraph
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, static_url_path="")
engine = create_engine("sqlite:///books.db")
DbSession = sessionmaker()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books")
def books():
    books = []
    session = DbSession(bind=engine)
    for b in session.query(Book).all():
        books.append({
            "Title": b.Title,
            "Rank": b.Rank,
            "Url": b.Url,
            "GutembergId": b.GutembergId,
            "Id": b.Id
        })
    return jsonify(books)

@app.route("/book/<id>")
@app.route("/book/<id>/content")
def content(id):
    paragraphs = []
    session = DbSession(bind=engine)
    for p in session.query(Paragraph).filter(Paragraph.BookId == id).all():
        paragraphs.append({
            "Value": p.Value
        })
    return jsonify(paragraphs)

if __name__== '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)


#if __name__ == '__main__':
    #print(get_books())
    #e = Epub("/home/vvv/Downloads/O Exterminador do Futuro - James Cameron.epub")
    #e.extract()
    #t = Translator()
    #p(t.translate("Gostaria que fallot 4 fosse tão maduro e cativante quanto Metro 2033", "russo"))
    #p(t.translate("Eu amei essa idéia!"))
    #p(t.translate("Eu amei essa idéia!", "francês"))
    #t.close()
