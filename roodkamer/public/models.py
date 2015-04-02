# -*- coding: utf-8 -*-
from roodkamer.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

import datetime as dt

class Article(SurrogatePK, Model):
    __tablename__ = "articles"
    title = Column(db.String(128), unique=True, nullable=False)
    body = Column(db.Text, nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    is_visible = Column(db.Boolean(), default=False)

    def __init__(self, title, visible=False, **kwargs):
        db.Model.__init__(self, title=title, is_visible=visible, **kwargs)

    def __repr__(self):
        return '<Article({title})>'.format(title=self.title)