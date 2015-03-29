# -*- coding: utf-8 -*-
import datetime as dt

from flask.ext.login import UserMixin

from roodkamer.extensions import bcrypt
from roodkamer.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)
from __builtin__ import staticmethod

class Permission:
    COMMENT = 0x01
    WRITE_ARTICLES = 0x02
    MODERATE_COMMENTS = 0x04
    VOTE = 0x08
    BLOCK = 0x10
    ADMINISTER = 0x80

class Role(SurrogatePK, Model):
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='roles')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    
    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    @staticmethod
    def insert_roles():
        roles = {
            'Observer': (Permission.COMMENT |
                         Permission.WRITE_ARTICLES, True),
            'Comrade': (Permission.COMMENT |
                        Permission.WRITE_ARTICLES |
                        Permission.MODERATE_COMMENTS |
                        Permission.VOTE |
                        Permission.BLOCK, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)

class User(UserMixin, SurrogatePK, Model):
    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=False)
    last_name = Column(db.String(30), nullable=False)
    active = Column(db.Boolean(), default=True)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, fname, lname, password, **kwargs):
        db.Model.__init__(self, username=username, email=email, first_name=fname, last_name=lname, **kwargs)
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)
