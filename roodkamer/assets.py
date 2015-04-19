# -*- coding: utf-8 -*-
from flask.ext.assets import Bundle, Environment

css = Bundle(
    "libs/bootstrap/dist/css/bootstrap.css",
    "css/style.css",
    "css/bootstrap-multiselect.css",
    "css/bootstrap-tagsinput.css",
    "css/selectize.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "libs/ajax/ckeditor/ckeditor.js",
    "js/plugins.js",
    "js/bootstrap-multiselect.js",
    "js/bootstrap-tagsinput.js",
    "js/selectize.js",
    "js/script.js",
    filters='jsmin',
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
