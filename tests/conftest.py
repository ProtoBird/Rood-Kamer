# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import os

import pytest
from webtest import TestApp
from .factories import UserFactory, ArticleFactory, TagFactory
from sqlalchemy.exc import InvalidRequestError

from roodkamer.settings import TestConfig
from roodkamer.app import create_app
from roodkamer.database import db as _db
from roodkamer.user.models import Role


@pytest.yield_fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


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
