from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.widgets import TextArea
from wtforms.fields import TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length

from roodkamer.user.models import User

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)
 
 
class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget() 

class ArticleForm(Form):
    title = TextField('Title',
                      validators=[DataRequired(), Length(min=3, max=128)])
    authors = SelectMultipleField('Author(s)',
                         validators=[DataRequired()])
    body = CKTextAreaField()
    post = SubmitField()