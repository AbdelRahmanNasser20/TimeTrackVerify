# scripts/create_db.py
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Employee, Event

# Set the environment variable or hardcode the SQLALCHEMY_DATABASE_URI
SQLALCHEMY_DATABASE_URI = "postgres://u7rjm4v00r7o80:p29318c85fd890024aabb5af0d2eee671f3b489fceb0846bc261184455c66a610@cb5ajfjosdpmil.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dcbccjj9ki7jbl"

# Optionally, set it as an environment variable to be used by the Flask app

config_name = os.getenv('FLASK_ENV')  # Assuming this is set for other configurations
app = create_app(config_name)


with app.app_context():
    # Create the connection and ensure the tables are created
    try:
        # Drop existing tables and create new ones
        db.drop_all()
        db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")
