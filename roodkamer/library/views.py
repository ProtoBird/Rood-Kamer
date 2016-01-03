# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required

from roodkamer.library.models import Book, Author, Publisher

blueprint = Blueprint("library", __name__, url_prefix='/library',
                      static_folder="../static")
