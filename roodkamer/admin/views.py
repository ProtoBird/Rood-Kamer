# -*- coding: utf-8 -*-
from flask.ext.admin import expose
from flask.ext.admin.base import  AdminIndexView


class RkAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return super(RkAdminView, self).index()