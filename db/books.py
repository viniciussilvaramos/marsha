from db.model import Book, Paragraph
from sqlalchemy.orm import sessionmaker, join

class BooksDB(object):

    def __init__(self, engine):
        self.dbSession = sessionmaker()
        self.engine = engine
    
    def _get_session(self):
        return self.dbSession(bind=self.engine)
    
    def all(self):
        books = []
        session = self._get_session()
        try:
            for b in session.query(Book).all():
                books.append({
                    "Title": b.Title,
                    "Rank": b.Rank,
                    "Url": b.Url,
                    "Id": b.Id
                })
        finally:
            session.close()

        return books        
    
    def content(self, book_id):
        session = self._get_session()
        try:
            content = session.query(Paragraph.Value, Book.Title).\
                join(Paragraph.Book).\
                filter(Paragraph.BookId == book_id).\
                all()

            book = {
                "Title": content[0][1],
                "Content": [p[0] for p in content]
            }

        finally:
            session.close()

        return book

