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
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('library_authors.id'))  
)


class Book(SurrogatePK, Model):
    __tablename__ = "books"
    
    title = Column(db.String(128), unique=False, nullable=False)
    authors = db.relationship('Author',
                              secondary=author_book_table,
                              backref=db.backref('books', lazy='dynamic'))
    # One User can check out many books; 1 book may only be checked out
    # by one person. This does not apply for e-books, of course.
    possession_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                              nullable=True)
    inPossessionOf = db.relationship('User', backref='books_checked_out',
                                     foreign_keys=[possession_id])
    
    isDeadTree = Column(db.Boolean, nullable=False)
    pages = Column(db.Integer, nullable=True)
    bookType = Column(db.String(64), nullable=False)
    publicationDate = Column(db.DateTime,
                             nullable=True,
                             default=None)
    originalPublicationDate = Column(db.DateTime,
                             nullable=True,
                             default=None)
    publishedBy = Column(db.Integer, db.ForeignKey('publishers.id'))
    isbn = Column(db.String(10), unique=True, nullable=True, default=None)
    isbn13 = Column(db.String(13), unique=True, nullable=True, default=None)
    
    termOfLoan = Column(db.Date, nullable=True)
    conditionOfLoan = Column(db.Text, nullable=True)
    loaned_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    loanedBy = db.relationship('User', backref='books_loaned', 
                               foreign_keys=[loaned_id])

    def __repr__(self):
        return '<Book({title} by {authors})>'.format(
            name=self.name,
            authors=",".join(self.authors)
        )
     

class Author(SurrogatePK, Model):
    __tablename__ = "library_authors"
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
    books_published = db.relationship('Book',
                                  backref='book',
                                  lazy='dynamic') 

    def __repr__(self):
        return '<Publisher({name})>'.format(name=self.name)
