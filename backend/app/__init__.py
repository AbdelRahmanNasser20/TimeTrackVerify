from flask import Flask, send_from_directory

from flask_cors import CORS
from .config import config_by_name
from .extensions import db, migrate
from .routes import api
import os
# import os , sys

# print("ALL DIRECTORIES ", os.path.dirname(__file__))
# print("BEFORE", sys.path)
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
# print("AFTER: sys.path after appending backend directory:", sys.path)

# # Load environment variables from the .env file in the timetrack Verify directory
# dotenv_loaded = load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
# # print("SECOND: dotenv loaded:", dotenv_loaded)

# print("ALL DIRECTORIES ", os.path.dirname(__file__))
# print("BEFORE", sys.path)


def create_app(config_name='development'):
    
    
    current_working_directory = os.getcwd()

    # Go to the parent directory of the current working directory
    parent_directory = os.path.abspath(os.path.join(current_working_directory, '..'))

    # Define the path to the React build folder relative to TimeTrackVerify
    static_folder_path = os.path.join(parent_directory, 'front', 'build')
    print("Resolved static folder path:", static_folder_path)


    # Initialize Flask with the correct static folder
    app = Flask(__name__, static_folder=static_folder_path, static_url_path='/')
    app.config.from_object(config_by_name[config_name])
    print("Resolved static folder path:", os.path.exists(static_folder_path))
    print("Static folder being used:", app.static_folder)
    # Serve React App for all other routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):        
        return send_from_directory(app.static_folder, 'index.html')
    
    CORS(app)

    # app = Flask(__name__)    
    # app.config.from_object(config_by_name[config_name])
    

    # Initialize ext
    # ensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(api)
        
        
    return app
