from flask import Flask
from .api.routes import api
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from .web.routes import web

db = SQLAlchemy()

def commify_filter(value):
    try:
        return f"{int(value):,d}"
    except (TypeError, ValueError):
        return value

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api, url_prefix='/api/')
    app.register_blueprint(web, url_prefix='/')

    db.init_app(app)

    app.add_template_filter(commify_filter, 'commify')

    return app