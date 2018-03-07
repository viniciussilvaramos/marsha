from db.books import BooksDB
from translator import Translator
from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine

app = Flask(__name__, static_url_path="")
engine = create_engine("sqlite:///books.db")
books_db = BooksDB(engine)
translator = Translator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books")
def get_books():
    books = books_db.all() 
    return render_template("books.html", books=books)

@app.route("/book/<id>/content")
def content(id):
    book = books_db.content(id)
    return render_template("content.html", Title=book["Title"], Content=book["Content"])

@app.route("/translate")
def translate():
    return translator.translate("Eu amei essa idéia!", "russo")

if __name__== '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)