# scripts/populate_db.py
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Employee, Event

app = create_app('development')

with app.app_context():
    # Add sample users
    user1 = User(username='john_doe', email='john@example.com')
    user2 = User(username='jane_doe', email='jane@example.com')
    db.session.add(user1)
    db.session.add(user2)

    # Add sample employees
    employee1 = Employee(name='John Smith', email='john.smith@example.com')
    employee2 = Employee(name='Jane Doe', email='jane.doe@example.com')
    db.session.add(employee1)
    db.session.add(employee2)

    # Add sample events
    event1 = Event(employee_id=employee1.id, name='Conference', date='2024-07-16', duration='2 hours', position='Speaker', location='Room 101')
    event2 = Event(employee_id=employee2.id, name='Workshop', date='2024-07-17', duration='3 hours', position='Trainer', location='Room 202')
    db.session.add(event1)
    db.session.add(event2)

    db.session.rollback()    
    print("Database populated successfully.")
