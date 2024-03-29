# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from flask import url_for, current_app
from webtest.app import AppError

from roodkamer.public.views import load_user 
from roodkamer.user.models import User
from roodkamer.media.models import Article, Tag
from .factories import UserFactory, ArticleFactory, TagFactory


class TestLoggingIn:

    def test_can_log_in_returns_200(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert "Invalid password" in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert "Unknown user" in res


class TestRegistering:

    def test_can_register(self, user, testapp):
        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get("/")
        # Clicks Create Account button
        res = res.click("Create account")
        # Fills out the form
        form = res.forms["registerForm"]
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_passwords_dont_match(self, user, testapp):
        # Goes to registration page
        res = testapp.get(url_for("public.register"))
        # Fills out form, but passwords don't match
        form = res.forms["registerForm"]
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secrets'
        # Submits
        res = form.submit()
        # sees error message
        assert "Passwords must match" in res

    def test_see_error_message_if_user_already_registered(self, user, testapp):
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = testapp.get(url_for("public.register"))
        # Fills out form, but username is already registered
        form = res.forms["registerForm"]
        form['username'] = user.username
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit()
        # sees error
        assert "Username already registered" in res


class TestArticleSubmission:

    def test_can_submit_new_article(self, article, testapp, user):
        # login sequence
        # TODO: Make DRY
        reslogin = testapp.get("/")
        loginForm = reslogin.forms['loginForm']
        loginForm['username'] = user.username
        loginForm['password'] = 'myprecious'
        # Submits
        reslogin = loginForm.submit().follow()
        assert reslogin.status_code == 200

        # New articles are identified by having id=0
        res = testapp.get(url_for('media.edit_article', artid=0))
        form = res.forms['articleForm']
        form['title'] = "Python: Now for Something Completely Different"
        form['authors'] = [user.id]
        form['body'] = "Unfinished artic"
        form['category'] = "Test Posts"

        #Submits
        res = form.submit().follow()
        assert res.status_code == 200
        assert "Article submitted!" in res


class TestArticleViewing:
    def test_can_edit_another_authors_article(self, 
                                              testapp, 
                                              authorship_scenario):
        author = authorship_scenario.author
        notAuthor = authorship_scenario.notAuthor
        anArticle = authorship_scenario.anArticle
    
        # login sequence
        # TODO: Make DRY
        reslogin = testapp.get("/")
        loginForm = reslogin.forms['loginForm']
        loginForm['username'] = notAuthor.username
        loginForm['password'] = "literaryRef42"
        # Submits
        reslogin = loginForm.submit().follow()
        assert reslogin.status_code == 200 
        res = None
        try:
            res = testapp.get("/media/edit_article/id_{}".format(author.id))
        except AppError as ae:
            # This is supposed to happen    
            status_code_401 = "401 UNAUTHORIZED"
            reason = "Only the currently listed authors may edit this article. "
            
            assert status_code_401 in ae.message
            assert reason in ae.message
        else:
            # This SHOULD have failed, so this success is A GOD DAMN FAILURE
            assert False