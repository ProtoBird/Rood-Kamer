# -*- coding: utf-8 -*-
from factory import Sequence, PostGenerationMethodCall, post_generation
from factory.alchemy import SQLAlchemyModelFactory

from roodkamer.user.models import User
from roodkamer.media.models import Article, Tag
from roodkamer.database import db


class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True

    class Meta:
        model = User


class ArticleFactory(BaseFactory):
    title = Sequence(lambda n: "Interesting Original Article #{0}".format(n))
    body = Sequence(lambda n: "In the course of blah #{0}...blah".format(n))
    category = "Test Posts"

    class Meta:
        model = Article

    @post_generation
    def subject_tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.subject_tags.append(tag)


class TagFactory(BaseFactory):
    name = Sequence(lambda n: "tag{0}".format(n))

    class Meta:
        model = Tag
