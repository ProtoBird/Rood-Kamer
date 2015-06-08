# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.widgets import TextArea
from wtforms.fields import TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields.core import BooleanField

from roodkamer.user.models import User


class CKTextAreaWidget(TextArea):
    """Widget for displaying WYSIWYG CK Editor
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)
 
 
class CKTextAreaField(TextAreaField):
    """Text area field WYSIWYG CK Editor
    
    Text area for plugging the `roodkamer.media.CKTextAreaWidget`
    into a `flask_wtf.Form`.
    
    Attributes:
        widget
    
    """
    widget = CKTextAreaWidget()


class ArticleForm(Form):
    """Article Form
    
    Form for writing new articles and editing published articles.
    
    """
    title = TextField('Title',
                      validators=[DataRequired(), Length(min=3, max=128)])
    authors = SelectMultipleField('Author(s)', validators=[DataRequired()],
                                  coerce=int)
    body = CKTextAreaField("Body", validators=[DataRequired()])
    category = SelectField('Category', 
                          validators=[DataRequired(), Length(min=3, max=80)])
    post = SubmitField("Post")
    is_visible = BooleanField("Publish")
    subject_tags = TextField("Tags")
    cancel = SubmitField("Cancel")
    
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(ArticleForm, self).validate()
        if not initial_validation:
            return False
        else:
            return True
