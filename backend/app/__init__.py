from flask import Flask
from flask_cors import CORS
from .config import config_by_name
from .extensions import db, migrate
from .routes import api

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(api)

    return app
