# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from roodkamer.user.models import User, Role
from roodkamer.media.models import Article
from .factories import UserFactory, ArticleFactory, TagFactory


@pytest.mark.usefixtures('db')
class TestUser:

    def test_get_by_id(self):
        user = User('foo', email='foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert user.password is None

    def test_factory(self, db):
        user = UserFactory(password="myprecious")
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self):
        user = User.create(username="foo", email="foo@bar.com",
                           password="foobarbaz123")
        assert user.check_password('foobarbaz123') is True
        assert user.check_password("barfoobaz") is False

    def test_full_name(self):
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"

    def test_default_role_is_observer(self):
        u = UserFactory()
        u.save()
        assert u.role.name == 'Observer'


@pytest.mark.usefixtures('db')
class TestArticle:
    def test_get_by_id(self):
        art = Article("On the nature of foo")
        art.save()

        retrieved = Article.get_by_id(art.id)
        assert retrieved == art

    def test_factory(self, db):
        artFact = ArticleFactory.create(subject_tags=[TagFactory(),
                                                      TagFactory()])
        db.session.commit()
        assert bool(artFact.title)
        assert bool(artFact.created_at)
        assert bool(artFact.subject_tags)
