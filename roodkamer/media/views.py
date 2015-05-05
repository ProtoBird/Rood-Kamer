# -*- coding: utf-8 -*-
'''Media section including articles and the management of images and video.'''
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    abort
)
from flask.ext.login import login_required
from sqlalchemy.exc import InvalidRequestError

from roodkamer.media.models import Article, tags, Tag, authors
from roodkamer.media.forms import ArticleForm
from roodkamer.user.models import User
from roodkamer.database import db
from roodkamer.utils import flash_errors
from roodkamer.media.utils import article_viewdb_generate

blueprint = Blueprint('media', __name__, url_prefix='/media',
                      static_folder="../static")

NEW_ARTICLE = 0


@login_required
@blueprint.route("/edit_article/id_<int:artid>", methods=['GET', 'POST'])
def edit_article(artid=NEW_ARTICLE):
    form = None

    tagdisplay, authdisplay = None, None
    article = Article.query.filter_by(id=artid).first()

    #Prepare edit article display with valid information
    if artid is not NEW_ARTICLE:
        if not article:
            flash("Article with id of {id} not found".format(id=artid))
            return redirect(url_for('media.view_article_db'))
        elif int(session["user_id"]) not in article.authors:
            msg = "Only the currently listed authors may edit this article. "
            msg += "You are not one of those authors."
            return render_template("401.html", reason=msg), 401
             
        else:
            form = ArticleForm(request.form, obj=article, csrf_enabled=False)
            tagdisplay = ', '.join([t.name for t in article.subject_tags])
            authdisplay = {u.username: u.id for u in article.authors}
    else:
        form = ArticleForm(request.form, csrf_enabled=False)

    #Setup choices for authors and categories from the database
    form.authors.choices = [(u.id, u.username)
                            for u in User.query.order_by('last_name')]
    q = db.session.query(Article.category.distinct().label('category'))
    form.category.choices = [(a.category, a.category) for a in q]

    if form.category.data and form.category.data not in form.category.choices:
        #This is to allow the user's typed option to become a valid choice
        form.category.choices.append((form.category.data, form.category.data))
    if form.cancel.data:
        return redirect(url_for('media.view_article_db'))

    #Article submission section
    if form.validate_on_submit():
        try:
            if article:
                #Edit an article
                article.authors = User.query.filter(
                    User.id.in_(form.data["authors"])).all()
                article.title = form.title.data
                article.body = form.body.data
                article.is_visible = form.is_visible.data
                article.category = form.category.data

                #Parse subject tag string into multiple tag object
                tagobjs = []
                for arttag in form.data["subject_tags"].split(","):
                    tagobj = Tag.query.filter_by(name=arttag).first()
                    if tagobj:
                        tagobjs.append(tagobj)
                    else:
                        tagobjs.append(Tag.create(name=arttag))
                article.subject_tags = tagobjs

                db.session.merge(article)
            else:
                #Create a new article
                article = Article.create(title=form.title.data,
                                         body=form.body.data,
                                         publish=form.is_visible.data,
                                         category=form.category.data)

                #Prepare author and subject tags for submission
                aids = [int(x) for x in form.authors.data]
                for aid in User.query.filter(User.id.in_(aids)):
                    article.authors.append(aid)
                for tagstr in form.subject_tags.data.split(","):
                    #check to see if each tag is in DB,
                    #if not add as a new Tag object
                    taginDB = Tag.query.filter_by(name=tagstr).first()
                    article.subject_tags.append(taginDB) if taginDB\
                        else article.subject_tags.append(Tag(name=tagstr))
                db.session.add(article)
            db.session.commit()
            flash("Article submitted!", "success")
        except InvalidRequestError as ire:
            db.session.rollback()
            db.session.flush()
            flash("Database error encountered. Article was not saved.",
                  "failure")
        return redirect(url_for('media.view_article_db'))
    else:
        flash_errors(form)
    return render_template(
        "media/edit.html",
        post_form=form,
        tags=tagdisplay,
        auths=authdisplay
    )


@login_required
@blueprint.route("/view_article_db/", methods=["GET"])
def view_article_db():
    arts = Article.query.filter().all()
    articles = article_viewdb_generate(arts)
    return render_template("media/view_article_db.html", articles=articles,
                           uid=session["user_id"])
