from flask import Flask, url_for
from importlib import import_module

def register_blueprints(app):
    for module_name in ('base', 'threats'):
        module=import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app():
    app=Flask(__name__, static_folder='base/static', template_folder='base/templates')
    register_blueprints(app)
    return app