# scripts/create_db.py
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Employee, Event

app = create_app('development')

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Tables created successfully.")