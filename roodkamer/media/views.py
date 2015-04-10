# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required

from roodkamer.media.models import Article, tags, Tag
from roodkamer.media.forms import ArticleForm
from roodkamer.user.models import User
from roodkamer.database import db
from roodkamer.utils import flash_errors

blueprint = Blueprint('media', __name__, url_prefix='/media', 
                      static_folder="../static")

@login_required
@blueprint.route("/edit_article/id_<int:artid>", methods=['GET', 'POST'])
def edit_article(artid=0):
    form = None
    tagdisplay, authdisplay = None, None
    
    if artid > 0:
        article = Article.query.filter_by(id=artid).first()
        if not article: 
            flash("Article with id of {id} not found".format(id=artid))
            return redirect(url_for('media.view_article_db'))
        else:
            form = ArticleForm(request.form, obj=article, csrf_enabled=False)
            tagdisplay = ", ".join(article.subject_tags)
            authdisplay = ", ".join(article.authors)
            #form.subject_tags = [a.name for a in article.subject_tags] 
    else:
        form = ArticleForm(request.form, csrf_enabled=False)
        uid = int(session['user_id'])
        assert(uid in [x[0] for x in form.authors.choices])
        #TODO: Get the default to actually work
        form.authors.default = [uid]
    form.authors.choices = [(u.id, u.full_name) for u in User.query.order_by('last_name')]    
    if form.cancel.data:
        return redirect(url_for('media.view_article_db'))
    elif form.validate_on_submit():
        article = Article.create(title=form.title.data,
                                 body=form.body.data,
                                 publish=form.is_visible.data)
        aids = [int(x) for x in form.authors.data]
        for aid in User.query.filter(User.id.in_(aids)):
            article.authors.append(aid)
        for tagstr in form.subject_tags.data.split(","):
            taginDB = Tag.query.filter_by(name=tagstr).first()
            article.subject_tags.append(taginDB) if taginDB else article.subject_tags.append(Tag(name=tagstr)) 
        db.session.add(article)
        db.session.commit()
        flash("Article submitted!", "success")
        return redirect(url_for('media.view_article_db'))
    else:
        flash_errors(form)
    return render_template("media/edit.html", post_form=form, tagdisplay=tagdisplay, authdisplay=authdisplay)

@login_required
@blueprint.route("/view_article_db/", methods=["GET"])
def view_article_db():
    arts = Article.query.filter().all()
    articles = []
    for art in arts:
        article = {}
        article["title"] = art.title
        article["authors"] = ", ".join(art.authors)
        article["tags"] = ", ".join(art.subject_tags)
        article["published"] = art.is_visible
        article["timestamp"] = art.created_at.ctime()
        articles.append((article, art.id)) 
    return render_template("media/view_article_db.html", articles=articles)