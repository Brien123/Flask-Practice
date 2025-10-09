from flask import Flask

from .api.routes import api
from .config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api, url_prefix='/api/')

    db.init_app(app)

    # Register blueprints here

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
