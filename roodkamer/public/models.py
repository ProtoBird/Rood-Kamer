from roodkamer.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

class Article(SurrogatePK, Model):
    __tablename__ = "articles"
    def __init__(self, title, **kwargs):
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        return '<Article({title})>'.format(name=self.title)