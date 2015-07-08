# -*- coding: utf-8 -*-
"""Forms for roodkamer media and articles
"""

from flask_wtf import Form
from wtforms import TextField
from wtforms.widgets import TextArea
from wtforms.fields import TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields.core import BooleanField, StringField
from wtforms.fields.simple import SubmitField

from roodkamer.user.models import User
from roodkamer.media.models import Article

class CKTextAreaWidget(TextArea):
    """Widget for displaying WYSIWYG CK Editor
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditorCKTextAreaField')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    """Text area field WYSIWYG CK Editor

    Text area for plugging the `roodkamer.media.CKTextAreaWidget`
    into a :class:`~flask_wtf.Form`.

    Attributes:
        widget (:class:`~roodkamer.media.forms.CKTextAreaWidget`): Pluggin
            location for the CK Text widget.

    """
    widget = CKTextAreaWidget()


class ArticleForm(Form):
    """Article Form

    Form for writing new articles and editing published articles.

    Attributes:
        title (:class:`~wtforms.fields.StringField`): This is the title field.
            It is required, and must contain no less than 3 characters and no
            more than 128. Title is validated for uniqueness.
        authors (:class:`~wtforms.fields.SelectMultipleField`): This is the
            field which specifies the author and co-authors of the article. The
            selections are based on usernames, with the first listed considered
            the author and the rest are considered co-authors. All users listed
            as authors have permission to edit the article. At least one author
            is required.
        body (:class:`~roodkamer.media.forms.CKTextAreaField`): This is the
            field for the article text and other media.
        category (:class:`wtforms.fields.SelectField`): This is the field for
            selecting which category an article belongs in. Categories may be
            selected from database of existing articles or a new one can be
            inserted on article creation. This field is required.
        post (:class:`wtforms.fields.SubmitField`): Submit button. For
            submitting an article.
        cancel (:class:`wtforms.fields.SubmitField`): Cancel button. For not
            submitting an article.
        is_visible (:class:`~wtforms.fields.BooleanField`): A checkbox for
            determining if the article is displayed on the site.
        subject_tags (:class:`~wtforms.fields.StringField`): A text input
            modified with bootrap-tagsinput script for any number of
            identifying tags to be associated with the article.

    """
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=3, max=128)])
    authors = SelectMultipleField('Author(s)', validators=[DataRequired()],
                                  coerce=int)
    body = CKTextAreaField("Body")
    category = SelectField('Category',
                           validators=[DataRequired(), Length(min=3, max=80)])
    post = SubmitField("Post")
    is_visible = BooleanField("Publish")
    subject_tags = StringField("Tags")
    cancel = SubmitField("Cancel")

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validation function for submitting/editing Articles
        
        An extension of :func:`~flaskwtf.Form.validate`. The extension checks
        for duplicate titles.
        
        Returns:
            True if the inherited validation function does and the title
            submitted does not conflict with the title of another 
            :class:`~roodkamer.media.models.Article`, False otherwise.
        
        """
        initial_validation = super(ArticleForm, self).validate()
        if not initial_validation:
            return False

        # Make sure that title is unique
        article = Article.query.filter_by(title=self.title.data).first()
        if article:
            self.title.errors.append("Title already in use")
            return False
        else:
            return True