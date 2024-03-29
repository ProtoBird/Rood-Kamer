# -*- coding: utf-8 -*-
""" SQLAlchemy models for media object

This module contains the classes in the media package which are descendants 
of the SQLAlchemy Model class, and association tables of relationships between
said classes. 

Attributes:
    tags (:class:`~sqlalchemy.Table`): Association table between
        :class:`Tag` and :class:`Article`.
    authors (:class:`~sqlalchemy.Table`): Association table between
        :class:`Article` and :class:`roodkamer.user.models.User`.

"""

from roodkamer.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

import datetime as dt
from roodkamer.user.models import User


tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('articles_id', db.Integer, db.ForeignKey('articles.id'))
)

authors = db.Table(
    'authors',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('articles_id', db.Integer, db.ForeignKey('articles.id'))
)


class Tag(Model):
    """Keywords associated with :class:`Article`.
    
    Tags are strings which are associated with articles in a many-to-many 
    relationship. These strings aid in searches, and indicate keywords within
    an :class:`Article`.
    
    Attributes:
        id (:class:`~sqlalchemy.Column`): An unique integer ID.
        name (:class:`~sqlalchemy.Column`): A 64-maximum, unique character
            string, which represents a keyword. 
    
    """
    id = db.Column(db.Integer, primary_key=True)
    name = Column(db.String(64), unique=True, nullable=False)

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Tag({name})>'.format(name=self.name)

    @classmethod
    def get_all(cls, order="name"):
        return cls.query.order_by(order).all()


class Article(SurrogatePK, Model):
    __tablename__ = "articles"
    title = Column(db.String(128), unique=True, nullable=False)
    authors = db.relationship(
        'User',
        secondary=authors,
        backref=db.backref('articles', lazy='dynamic'),
        single_parent=True
    )
    category = Column(db.String(80))
    body = Column(db.Text, nullable=True)
    created_at = Column(
        db.DateTime,
        nullable=False,
        default=dt.datetime.utcnow
    )
    is_visible = Column(db.Boolean(), default=False)
    subject_tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('articles', lazy='dynamic'),
        single_parent=True,
        cascade="all,delete,delete-orphan"
    )

    def __init__(self, title, publish=False, **kwargs):
        db.Model.__init__(self, title=title, is_visible=publish, **kwargs)

    def __repr__(self):
        return '<Article({title})>'.format(title=self.title)
