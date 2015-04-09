# -*- coding: utf-8 -*-
from roodkamer.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
    association_proxy,
)

import datetime as dt
from roodkamer.user.models import User

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('articles_id', db.Integer, db.ForeignKey('articles.id'))
)

authors = db.Table('authors',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('articles_id', db.Integer, db.ForeignKey('articles.id'))
)

class Article(SurrogatePK, Model):
    __tablename__ = "articles"
    title = Column(db.String(128), unique=True, nullable=False)
    authors_rel = db.relationship('User', secondary=authors,
                                  backref=db.backref('articles', lazy='dynamic'),
                                  single_parent=True,
                                  cascade="all,delete,delete-orphan")
    authors = association_proxy('authors_rel', 'username',
                            creator=lambda auth: User(username=auth))
    body = Column(db.Text, nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    is_visible = Column(db.Boolean(), default=False)
    subject_tags_rel = db.relationship('Tag', secondary=tags,
        backref=db.backref('articles', lazy='dynamic'),
        single_parent=True,
        cascade="all,delete,delete-orphan")
    subject_tags = association_proxy('subject_tags_rel', 'name',
                            creator=lambda tagname: Tag(name=tagname))
    def __init__(self, title, publish=False, **kwargs):
        db.Model.__init__(self, title=title, is_visible=publish, **kwargs)

    def __repr__(self):
        return '<Article({title})>'.format(title=self.title)

class Tag(Model):
    id = db.Column(db.Integer, primary_key=True)
    name = Column(db.String(64), unique=True, nullable=False)

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)
        
    def __repr__(self):
        return '<Tag({name})>'.format(name=self.name)