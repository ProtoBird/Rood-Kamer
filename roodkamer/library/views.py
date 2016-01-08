# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required

from roodkamer.library.models import Book, Author, Publisher
from roodkamer.user.models import User, Permission
from roodkamer.decorators import permissions_required

blueprint = Blueprint("library", __name__, url_prefix='/library',
                      static_folder="../static")

from flask.views import MethodView
from flask.ext.login import login_required


class LibraryMain(MethodView):
    decorators = [login_required]

    @permissions_required(Permission.CHECK_OUT_BOOK)
    def get(self):
        return render_template("library/main.html")


class LoanBook(MethodView):
    decorators = [login_required]
    
    @permissions_required(Permission.CHECK_OUT_BOOK)
    def get(self):
        return render_template("library/loan_book.html")

blueprint.add_url_rule(
    "/main/", 
    view_func=LibraryMain.as_view("main"))
