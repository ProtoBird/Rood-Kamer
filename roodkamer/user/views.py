# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session
from flask.ext.login import login_required
from roodkamer.user.models import User

blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    u = User.query.filter_by(id=session["user_id"]).first()
    return render_template("users/members.html", username=u.username)