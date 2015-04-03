from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.widgets import TextArea
from wtforms.fields import TextAreaField
from wtforms.validators import DataRequired

from roodkamer.user.models import User

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)
 
 
class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget() 

class ArticleForm(Form):
    body = CKTextAreaField()
    post = SubmitField()