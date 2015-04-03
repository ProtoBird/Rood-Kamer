# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required

from roodkamer.public.models import Article
from roodkamer.public.forms import LoginForm, ArticleForm
from roodkamer.database import db

blueprint = Blueprint('media', __name__, url_prefix='/media', 
                      static_folder="../static")

@login_required
@blueprint.route("/edit_article/", methods=['GET', 'POST'])
def edit_article():
    form = ArticleForm(request.form, csrf_enabled=False)
    if request.method == "POST":
        pass
    return render_template("media/test.html", post_form=form)