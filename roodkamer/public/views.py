# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, session)
from flask.ext.login import login_user, login_required, logout_user

from roodkamer.extensions import login_manager
from roodkamer.user.models import User
from roodkamer.public.forms import LoginForm
from roodkamer.user.forms import RegisterForm
from roodkamer.utils import flash_errors
from roodkamer.database import db
from roodkamer.media.models import Article

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                               email=form.email.data,
                               password=form.password.data,
                               first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               active=False)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route("/articles/")
def articles():
    published_articles = Article.query.filter_by(is_visible=True).all()
    return render_template("public/articles.html", articles=published_articles)


@blueprint.route("/articles/id_<int:artid>")
def view_article(artid):
    article = Article.query.filter_by(id=artid).first()
    authors = ", ".join([auth.username for auth in article.authors])
    return render_template("public/view_article.html",
                           article=article,
                           authors=authors)