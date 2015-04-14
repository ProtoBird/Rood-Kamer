# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required
from roodkamer.civic.models import Proposal

blueprint = Blueprint("civic", __name__, url_prefix='/civic',
                        static_folder="../static")