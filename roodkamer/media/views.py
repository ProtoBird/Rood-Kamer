# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required

from roodkamer.media.models import Article
from roodkamer.media.forms import ArticleForm
from roodkamer.user.models import User
from roodkamer.database import db

blueprint = Blueprint('media', __name__, url_prefix='/media', 
                      static_folder="../static")

@login_required
@blueprint.route("/edit_article/", methods=['GET', 'POST'])
def edit_article():
    form = ArticleForm(request.form, csrf_enabled=False)
    form.authors.choices = [(u.id, u.full_name) for u in User.query.order_by('last_name')]
    uid = int(session['user_id'])
    assert(uid in [x[0] for x in form.authors.choices])
    form.authors.default = uid
    if request.method == "POST":
        pass
    return render_template("media/edit.html", post_form=form)