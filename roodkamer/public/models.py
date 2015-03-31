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
        title = Column(db.String(128), unique=True, nullable=False)
        body = Column(db.Text)
        created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __repr__(self):
        return '<Article({title})>'.format(name=self.title)