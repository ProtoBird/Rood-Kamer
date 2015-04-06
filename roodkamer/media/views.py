# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required

from roodkamer.media.models import Article, tags, Tag
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
    #TODO: Get the default to actually work
    form.authors.default = uid
    if request.method == "POST":
        #TODO: Setup validation
        article = Article.create(title=form.title.data,
                                 body=form.body.data)
        aids = [int(x) for x in form.authors.data]
        for aid in User.query.filter(User.id.in_(aids)):
            article.authors.append(aid)
        for tagstr in form.subject_tags.data.split(","):
            taginDB = Tag.query.filter_by(name=tagstr).first()
            article.subject_tags.append(taginDB) if taginDB else article.subject_tags.append(Tag(name=tagstr)) 
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('user.members'))
    return render_template("media/edit.html", post_form=form)