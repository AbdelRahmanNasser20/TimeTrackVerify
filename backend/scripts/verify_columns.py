import sys
import os
from sqlalchemy import text

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Employee

app = create_app('development')

def verify_columns():
    with app.app_context():
        # Verify columns in 'employees' table
        query = text("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'employees';
        """)
        
        result = db.session.execute(query)
        columns = result.fetchall()
        
        if columns:
            print("Columns in 'employees' table:")
            for column in columns:
                print(f"Column: {column[0]}, Data Type: {column[1]}")
        else:
            print("No columns found or table 'employees' does not exist.")

        # Fetch and display all employees
        employees = Employee.query.all()
        if employees:
            print("\nEmployees in 'employees' table:")
            for employee in employees:
                print(f"ID: {employee.id}, Name: {employee.name}, Email: {employee.email}, Phone: {employee.phone_number}")
        else:
            print("No employees found in 'employees' table.")

if __name__ == '__main__':
    verify_columns()
