# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import os
from collections import namedtuple

import pytest
from webtest import TestApp
from .factories import UserFactory, ArticleFactory, TagFactory
from sqlalchemy.exc import InvalidRequestError

from roodkamer.settings import TestConfig
from roodkamer.app import create_app
from roodkamer.database import db as _db
from roodkamer.user.models import Role
from aptdaemon.errors import NotAuthorizedError


@pytest.yield_fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app, extra_environ={'wsgi.url_scheme': 'https'})


@pytest.yield_fixture(scope='function')
def db(app):
    _db.app = app
    try:
        with app.app_context():
            _db.create_all()
            Role.insert_roles()
    except InvalidRequestError as ire:
        _db.session.rollback()
        _db.session.flush()
    finally:

        yield _db

        _db.drop_all()


@pytest.fixture
def user(db):
    user = UserFactory(password='myprecious')
    db.session.commit()
    return user


@pytest.fixture
def article(db):
    article = ArticleFactory.create(subject_tags=[TagFactory(),
                                                  TagFactory()],
                                    authors=[UserFactory(),
                                             UserFactory()])
    db.session.commit()
    return article


@pytest.fixture
def authorship_scenario(db):
    author = UserFactory(password="somepass1")
    notAuthor = UserFactory(password="literaryRef42")
    anArticle = ArticleFactory.create(subject_tags=[TagFactory()], 
                                      authors=[author])
    db.session.commit()
    scenario = namedtuple("AuthorshipScenario", ["author", 
                                                 "notAuthor", 
                                                 "anArticle"])
    scenario.author = author
    scenario.notAuthor = notAuthor
    scenario.anArticle = anArticle
    return scenario 