from flask import Flask
from flask_cors import CORS
from .config import config_by_name
from .extensions import db, migrate
from .routes import api

# import os , sys

# print("ALL DIRECTORIES ", os.path.dirname(__file__))
# print("BEFORE", sys.path)
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
# print("AFTER: sys.path after appending backend directory:", sys.path)

# # Load environment variables from the .env file in the timetrack Verify directory
# # dotenv_loaded = load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
# # print("SECOND: dotenv loaded:", dotenv_loaded)

# print("ALL DIRECTORIES ", os.path.dirname(__file__))
# print("BEFORE", sys.path)

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
