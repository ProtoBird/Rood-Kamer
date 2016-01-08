# -*- coding: utf-8 -*-
from flask.ext.admin import expose
from flask.ext.admin.base import  AdminIndexView
from flask.ext.login import current_user
from flask import abort

from roodkamer.decorators import permissions_required
from roodkamer.user.models import Permission


class RkAdminView(AdminIndexView):
    @permissions_required(Permission.ADMINISTER_WEB)
    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            abort(401)
        return super(RkAdminView, self).index()
