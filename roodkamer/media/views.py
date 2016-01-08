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
from flask.views import MethodView
from flask.ext.login import login_required
from sqlalchemy.exc import InvalidRequestError

from roodkamer.media.models import Article, tags, Tag, authors
from roodkamer.media.forms import ArticleForm
from roodkamer.user.models import User, Permission
from roodkamer.database import db
from roodkamer.utils import flash_errors
from roodkamer.media.utils import article_viewdb_generate
from roodkamer.decorators import permissions_required

blueprint = Blueprint('media', __name__, url_prefix='/media',
                      static_folder="../static")
NEW_ARTICLE = 0
class BadArticleIDException(Exception): pass
    
class SubmitArticle(MethodView):
    decorators = [login_required]
    def __init__(self):
        self.article = None
        self.form = None
        self.authdisplay = None
        self.tagdisplay = None
    
    @permissions_required(Permission.WRITE_ARTICLES)
    def get(self, artid=NEW_ARTICLE):
        """View for self.article submission.
    
        Function parameters should be documented in the ``Args`` section.
        The name of each parameter is required. The type and description
        of each parameter is optional, but should be included if not
        obvious.
    
        Args:
          artid (int, optional): This is the article id of the article 
            being edited. If no article id is supplied, the function
            will assume the article id is 0 (ie. NEW_ARTICLE).  

        Returns:
          pass! FORNOWOKLOL
    
        Raises:
          AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
          ValueError: If `param2` is equal to `param1`.
    
        """
        try:
            self.prep_view_objects(artid)
        except BadArticleIDException as baide:
            flash(baide.message)
            return redirect(url_for('media.view_article_db'))
        if self.form.cancel.data:
            return redirect(url_for('media.view_article_db'))
        
        return render_template("media/edit.html", 
                               post_form=self.form, 
                               tags=self.tagdisplay, 
                               auths=self.authdisplay)

    @permissions_required(Permission.WRITE_ARTICLES)
    def post(self, artid=NEW_ARTICLE):
        try:
            self.prep_view_objects(artid)
        except Badself.articleIDException as baide:
            flash(baide.message)
            return redirect(url_for('media.view_article_db')) 
        
        if self.form.validate_on_submit():
            try:
                if self.article:
                    # Edit an self.article
                    self.article.authors = User.query.filter(
                        User.id.in_(self.form.data["authors"])
                    ).all()
                    self.article.title = self.form.title.data
                    self.article.body = self.form.body.data
                    self.article.is_visible = self.form.is_visible.data
                    self.article.category = self.form.category.data
                    
                    # Parse subject tag string into multiple tag object
                    tagobjs = []
                    for arttag in self.form.data["subject_tags"].split(","):
                        tagobj = Tag.query.filter_by(name=arttag).first()
                        if tagobj:
                            tagobjs.append(tagobj)
                        else:
                            tagobjs.append(Tag.create(name=arttag))
                    self.article.subject_tags = tagobjs        
                            
                    db.session.merge(self.article)
                else: 
                    # Create a new self.article
                    self.article = Article.create(
                        title=self.form.title.data,
                        body=self.form.body.data,
                        publish=self.form.is_visible.data,
                        category=self.form.category.data
                    )
                    
                    # Prepare author and subject tags for submission
                    aids = [int(x) for x in self.form.authors.data]
                    for aid in User.query.filter(User.id.in_(aids)):
                        self.article.authors.append(aid)
                    for tagstr in self.form.subject_tags.data.split(","):
                        # check to see if each tag is in DB,
                        # if not add as a new Tag object
                        taginDB = Tag.query.filter_by(name=tagstr).first()
                        if taginDB:
                            self.article.subject_tags.append(taginDB)  
                        else:
                            self.article.subject_tags.append(Tag(name=tagstr)) 
                    db.session.add(self.article)
                db.session.commit()
                flash("Article submitted!", "success")
            except InvalidRequestError as ire:
                db.session.rollback()
                db.session.flush()
                flash("Database error encountered. Article was not saved.",
                      "failure")
            return redirect(url_for('media.view_article_db'))
        else:
            flash_errors(self.form)

    def prep_view_objects(self, artid):
        self.article = Article.query.filter_by(id=artid).first()
        
        # Prepare edit self.article display with valid inself.formation
        if artid is not NEW_ARTICLE:
            author_ids = [a.id for a in self.article.authors]
            if not self.article:
                msg = "Article with id of {id} not found".self.format(id=artid)
                raise BadArticleIDException(msg)
            elif int(session["user_id"]) not in author_ids:
                msg = "You are not authorized to edit this article."
                raise BadArticleIDException(msg)
            else:
                self.form = ArticleForm(request.form,
                                        obj=self.article, 
                                        csrf_enabled=False)
                self.tagdisplay = ', '.join(
                    [t.name for t in self.article.subject_tags]
                )
                self.authdisplay = {u.username: u.id 
                                    for u in self.article.authors}
        else:
            self.form = ArticleForm(request.form, csrf_enabled=False)
        
        # Setup choices for authors and categories from the database
        self.form.authors.choices = [
            (u.id, u.username) for u in User.query.order_by('last_name')
        ];    
        q = db.session.query(Article.category.distinct().label('category'))        
        self.form.category.choices = [(a.category, a.category) for a in q]
                    
        if self.form.category.data and (self.form.category.data not in 
                                   self.form.category.choices):
            # This is to allow the user's typed option to become a valid choice
            self.form.category.choices.append((self.form.category.data, 
                                          self.form.category.data))
        
        return


class ViewArticleDB(MethodView):
    decorators = [login_required]
    
    @staticmethod
    def article_viewdb_generate(arts):
        articles = []
        for art in arts:
            article = {}
            article["title"] = art.title
            article["authors"] = ", ".join([t.username for t in art.authors])
            article["authors_ids"] = [t.id for t in art.authors]
            article["category"] = art.category
            article["tags"] = ", ".join([t.name for t in art.subject_tags])
            article["published"] = art.is_visible
            article["timestamp"] = art.created_at.ctime()
            articles.append((article, art.id))
        return articles

    
    def get(self):
        arts = Article.query.filter().all()
        articles = article_viewdb_generate(arts) 
        return render_template("media/view_article_db.html",
                               uid=long(session["user_id"]),
                               articles=articles)

blueprint.add_url_rule(
    "/edit_article/id_<int:artid>", 
    view_func=SubmitArticle.as_view("edit_article")
)

blueprint.add_url_rule(
    "/view_article_db/", 
    view_func=ViewArticleDB.as_view("view_article_db"))
