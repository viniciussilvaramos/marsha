from db.books import BooksDB
from flask import Flask, render_template, jsonify
from json import loads
from helper.gutenberg import Gutenberg
from translator.selenium import Translator

app = Flask(__name__, static_url_path="")
with open("config.json") as f:
    db_uri = loads(f.read())["db_uri"]

books_db = BooksDB(db_uri)
t = Translator()
g = Gutenberg(books_db)
g.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books")
def get_books():
    books = []
    try:
        books = books_db.all() 
    except:
        return render_template("books.html", books=books)

@app.route("/book/<id>/content")
def content(id):
    book = books_db.content(id)
    return render_template("content.html", Title=book["Title"], Content=book["Content"])

# @app.route("/books/load")
# def load_from_gutemberg():
#     return g.start()

@app.route("/translate/<lang>/<text>")
def translate(text, lang):
    json = jsonify(t.translate(text, lang))
    return json

if __name__== '__main__':
    print("This implemnetation is not complete!")
    app.run(host='0.0.0.0',port=80, debug=True)