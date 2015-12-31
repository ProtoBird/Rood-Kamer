# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required

blueprint = Blueprint("library", __name__, url_prefix='/library',
                      static_folder="../static")
