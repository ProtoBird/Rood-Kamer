# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template

from roodkamer.admin.views import RkAdminView
from roodkamer.settings import ProdConfig
from roodkamer.assets import assets
from roodkamer.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
    images,
)
from roodkamer import public, user, civic, media, library

def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    
     # Normally would go in extensions, but pytest does not play nice with
    # Flask-Admin unless it is encapsulated in the create_app, (ie. here)
    from flask.ext.admin import Admin
    admin = Admin(name="RoodKamer", 
                  template_mode='bootstrap3',
                  index_view=RkAdminView())
    admin.init_app(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    images.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(civic.views.blueprint)
    app.register_blueprint(media.views.blueprint)
    app.register_blueprint(library.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
