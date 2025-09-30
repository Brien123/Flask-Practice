
from flask import Flask
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions here

    # Register blueprints here

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
