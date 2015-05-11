# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session
from flask.ext.login import login_required
from roodkamer.user.models import User
from roodkamer.media.models import Article
from roodkamer.media.utils import article_viewdb_generate

blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    u = User.query.filter_by(id=session["user_id"]).first()
    return render_template("users/members.html", username=u.username)


@blueprint.route("/profile.<username>")
@login_required
def profile(username):
    u = User.query.filter_by(id=session["user_id"]).first()
    uarticles = [art for art in Article.query.all() if u in art.authors]
    uarticles = article_viewdb_generate(uarticles)
    return render_template("users/profile.html", user=u,
                           uid=long(session["user_id"]), articles=uarticles)
