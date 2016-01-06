# -*- coding: utf-8 -*-
import datetime as dt
import sys

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
    VOTE = 0x04
    CHECK_OUT_BOOK = 0x08
    SCHEDULE_LASER = 0x10
    SCHEDULE_SHOPBOT = 0x20
    SCHEDULE_TORMACH = 0x40
    ADMINISTER_WEB = 0x80
    ALL = 0xff


class Role(SurrogatePK, Model):
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    default = db.Column(db.Boolean(create_constraint=False), default=False, 
                        index=True)
    permissions = db.Column(db.Integer)

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    @staticmethod
    def insert_roles():
        roles = {
            'Observer': (Permission.COMMENT, True),
            'Club Member': (Permission.COMMENT |
                        Permission.WRITE_ARTICLES |
                        Permission.VOTE |
                        Permission.CHECK_OUT_BOOK |
                        Permission.SCHEDULE_LASER, False),
            'Complete Member': (Permission.COMMENT |
                        Permission.WRITE_ARTICLES |
                        Permission.VOTE |
                        Permission.CHECK_OUT_BOOK |
                        Permission.SCHEDULE_LASER |
                        Permission.SCHEDULE_SHOPBOT | 
                        Permission.SCHEDULE_TORMACH, False),
            'Web Master': (Permission.ADMINISTER_WEB, False),
            'Board Member': (Permission.ALL, False),
        }
        
        try:
            assert [v[1] for v in roles.values()].count(True) == 1
            for r in roles:
                role = Role.query.filter_by(name=r).first()
                if role is None:
                    role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
        except AssertionError:
            defaults = [k for k,v in roles.items() if v[1]]
            msg = "There should be only 1 default, instead there are {0}"
            msg += ", namely: {1}.".format(len(defaults), defaults)
            sys.stderr.write(msg)
        db.session.commit()
    
    def assign_role(self, users):
        def add_user(user):
            user_roles_names = [r.name for r in user.roles.all()] 
            for user_role in user_roles_names:
                if self.name in user_roles_names:
                    msg = "User '{u}' already has Role '{r}'"
                    msg.format(u=user.username, r=self.name)
                    raise AttributeError(msg)
            user.roles.append(self)  
            db.session.add(user)
        try:
            for user in users:
                add_user(user)
        except TypeError:
            add_user(users)
        db.session.commit()
        
    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)

    def __str__(self):
        return self.name


class User(UserMixin, SurrogatePK, Model):
    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(
        db.DateTime,
        nullable=False,
        default=dt.datetime.utcnow
    )
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=True)
    is_admin = Column(db.Boolean(), default=False)
    roles = db.relationship('Role', backref='users', lazy='dynamic',
                            cascade="all, delete-orphan")
    books_checked_out = Column(db.Integer, db.ForeignKey('books.id'))

    def __init__(self, username, password=None, **kwargs):
        db.Model.__init__(self, username=username, **kwargs)
        if password:
            self.set_password(password)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)
    
    @classmethod
    def get_all(cls, order='last_name'):
        return cls.query.order_by(order).all()

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)
