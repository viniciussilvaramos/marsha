from sqlalchemy import Column, ForeignKey, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'

    Id = Column(Integer, primary_key=True)
    GutembergId = Column(Integer, nullable=False)
    Title = Column(String(), nullable=False)
    Url = Column(String(), nullable=False)
    Rank = Column(Integer, nullable=False)

class Paragraph(Base):
    __tablename__ = 'paragraph'

    Id = Column(Integer, primary_key=True)
    Value = Column(String(), nullable=False)
    BookId = Column(Integer, ForeignKey("book.Id"))
    Book = relationship(Book)

engine = create_engine('sqlite:///books.db')

Base.metadata.create_all(engine)