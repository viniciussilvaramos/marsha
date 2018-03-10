from db.model import Book, Paragraph, init
from sqlalchemy.orm import sessionmaker, join
from sqlalchemy import create_engine

class BooksDB(object):

    def __init__(self, db_uri):
        init(db_uri)
        self.engine = create_engine(db_uri)
        self.dbSession = sessionmaker()
    
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

    def save(self, book, paragraphs):
        session = self._get_session()
        try:
            b = Book(**book)
            session.add(b)

            for pl in paragraphs:
                p = Paragraph(Value=pl, Book=b)
                session.add(p)
            
            session.commit()
        except:
            session.rollback()
            print("Um erro ocorreu.")
        finally:
            session.close()

