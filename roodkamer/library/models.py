# -*- coding: utf-8 -*-
import datetime as dt
from roodkamer.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


author_book_table = db.Table(
    "authors_to_books",
    db.Column('book_id', db.Interger, db.ForeignKey('book.id')),
    db.Column('author_id', db.Interger, db.ForeignKey('author.id'))  
)


class Book(SurrogatePK, Model):
    __tablename__ = "books"
    
    title = Column(db.String(128), unique=True, nullable=False)
    authors = db.relationship('Author',
                              secondary=author_book_table,
                              backref=db.backref('books', lazy='dynamic'))
    # One User can check out many books; 1 book may only be checked out
    # by one person. This does not apply for e-books, of course.
    inPossessionOf = db.relationship('User', 
                                     backref='book', 
                                     lazy='dynamic',
                                     nullable=True)
    isDeadTree = Column(db.Boolean, nullable=False)
    pages = Column(db.Integer(), nullable=True)
    bookType = Column(db.String(64), nullable=False)
    publicationDate = Column(db.DateTime,
                             nullable=True,
                             default=None)
    originalPublicationDate = Column(db.DateTime,
                             nullable=True,
                             default=None)
    publishedBy = db.relationship('Publisher',
                                  backref='book',
                                  lazy=dynamic,
                                  nullable=True,
                                  default=None)
    isbn = Column(db.String(10), unqiue=True, nullable=True, default=None)
    isbn13 = Column(db.String(13), unique=True, nullable=True, default=None)

    def __repr__(self):
        return '<Book({title} by {authors})>'.format(
            name=self.name,
            authors=",".join(self.authors)
        )
     

class Author(SurrogatePK, Model):
    __tablename__ = "authors"
    first_name = Column(db.String(64), unique=False, nullable=True)
    last_name = Column(db.String(64), unique=False, nullable=False)

    def full_name(self):
        if self.first_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.last_name 

    def __repr__(self):
        return '<Author({name})>'.format(name=self.full_name())


class Publisher(SurrogatePK, Model):
    __tablename__ = "publishers"
    name = Column(db.String(128), unique=True, nullable=False)

    def __repr__(self):
        return '<Publisher({name})>'.format(name=self.name)

