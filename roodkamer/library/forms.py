# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField
from wtforms.fields import(
    SelectMultipleField, 
    SelectField, 
    IntegerField, 
    DateField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length
from wtforms.fields.core import BooleanField, StringField
from wtforms.fields.simple import SubmitField

from roodkamer.library.models import Book, Author, Publisher


class LoanForm(Form):
    book_title = StringField(
        'Title', 
        validators=[DataRequired(), Length(min=3, max=128)]
    )
    authors = SelectMultipleField('Author(s)', validators=[DataRequired()],
                                  coerce=int)
    pages = IntegerField('Pages')
    bookType = SelectField('Book Type')
    publicationDate = DateField('Publication Date')
    originalPublicationDate = DateField('Original Publication Date')
    publishedBy = SelectField('Publisher')
    isbn = StringField('ISBN', 
                       validators=[DataRequired(), Length(min=10, max=10)])
    isbn13 = StringField('ISBN-13', 
                       validators=[DataRequired(), Length(min=13, max=13)])
    
    termOfLoan = DateField("Term of Loan")
    conditionOfLoan = TextAreaField("Conditions of Loan")

    def __init__(self, *args, **kwargs):
        super(LoanForm, self).__init__(*args, **kwargs)
