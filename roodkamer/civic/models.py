# -*- coding: utf-8 -*-

from roodkamer.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

class Proposal(SurrogatePK, Model):
    __tablename__ = "proposals"
    
    title = Column(db.String(128), unique=True, nullable=False)
    body = Column(db.Text)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    last_considered = Column(db.DateTime, nullable=True, default=None)
    is_live = Column(db.Boolean(), default=False)
    supporters = relationship('users', backref='proposals')
    opponents = relationship('users', backref='proposals')
    
    def __init__(self, title, **kwargs):
        db.Model.__init__(self, title=title, **kwargs) 

    def __repr__(self):
        return '<Proposal({title})>'.format(title=self.title)