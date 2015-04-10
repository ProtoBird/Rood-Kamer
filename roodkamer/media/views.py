# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required

from roodkamer.media.models import Article, tags, Tag, authors
from roodkamer.media.forms import ArticleForm
from roodkamer.user.models import User
from roodkamer.database import db
from roodkamer.utils import flash_errors

from sqlalchemy.exc import InvalidRequestError

blueprint = Blueprint('media', __name__, url_prefix='/media', 
                      static_folder="../static")

@login_required
@blueprint.route("/edit_article/id_<int:artid>", methods=['GET', 'POST'])
def edit_article(artid=0):
    form = None

    tagdisplay, authdisplay = None, None
    article = Article.query.filter_by(id=artid).first()
    
    if artid > 0:
        if not article: 
            flash("Article with id of {id} not found".format(id=artid))
            return redirect(url_for('media.view_article_db'))
        else:
            form = ArticleForm(request.form, obj=article, csrf_enabled=False)
            tagdisplay = ", ".join(article.subject_tags)
            authdisplay = ", ".join(article.authors)
    else:
        form = ArticleForm(request.form, csrf_enabled=False)
    form.authors.choices = [(u.id, u.full_name) for u in User.query.order_by('last_name')]    
    if form.cancel.data:
        return redirect(url_for('media.view_article_db'))
    elif form.validate_on_submit():
        try:
            if article:
                ud = {k:v for k,v in form.data.iteritems() if k not in ("post", "cancel", "subject_tags", "authors")}
                tgs = form.data["subject_tags"].split(",")
                article.subject_tags = [tid for tid in Tag.query.filter(Tag.name.in_(tgs))]
                article.authors = [aid for aid in User.query.filter(User.id.in_(form.data["authors"]))] 
                article.query.filter_by(id=artid).update(ud)
                
    #             article.authors = [aid for aid in User.query.filter(User.id.in_(form.data["authors"]))]
    #             article.subject_tags = form.data["subject_tags"].split(",")
    #             db.session.merge(article)
            else: 
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
        except InvalidRequestError as ire:
            db.session.rollback()
            db.session.flush()
        flash("Article submitted!", "success")
        return redirect(url_for('media.view_article_db'))
    else:
        flash_errors(form)
    return render_template("media/edit.html", post_form=form)

@login_required
@blueprint.route("/view_article_db/", methods=["GET"])
def view_article_db():
    arts = Article.query.filter().all()
    articles = []
    for art in arts:
        article = {}
        article["title"] = art.title
        article["authors"] = art.authors
        article["tags"] = art.subject_tags
        article["published"] = art.is_visible
        article["timestamp"] = art.created_at.ctime()
        articles.append((article, art.id)) 
    return render_template("media/view_article_db.html", articles=articles)