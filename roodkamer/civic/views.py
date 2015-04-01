# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required

blueprint = Blueprint("civic", __name__, url_prefix='/civic',
                        static_folder="../static")