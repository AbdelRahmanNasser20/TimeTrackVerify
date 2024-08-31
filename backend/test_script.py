import os
import requests
import psycopg2
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Employee, Event
from app.db_queries import get_employee_id

# Function to print all environment variables
def print_env_variables():
    print("Environment Variables:")
    for key, value in os.environ.items():
        print(f"{key} = {value}")
    print("\n")

# Test the backend API
def test_api():
    api_url = os.getenv('API_URL', 'http://backend:5001/verify')  # Use the service name 'backend'
    email = "abdel.nasser045@gmail.com"
    data = {
        "email": email,
        "tableData": [             
                    {"date": '2023-12-03', "hours": 2.25, "location": 'Good Shepherd ', "position": 'Teacher - Lead'} ,            
                    {"date": '2023-12-04', "hours": 2, "location": 'Oakland Terrace ES', "position": 'Teacher - Lead'},                
                    {"date": '2023-12-05', "hours": 2.75, "location": 'Burning Tree ES', 'position': 'Teacher - Assistant'},
                    {"date": '2023-12-06', "hours": 2.5, "location": 'Forest knolls ES', "position": 'Teacher - Lead'} ,
                    {"date": '2023-12-11', "hours": 2.5, "location": 'ST andrew', "position": 'Teacher - Lead'},
        ]
    }
    id = get_employee_id(email)
    print(" the email for ", email , " with employee id " , id)


    try:
        response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        if response.status_code == 200:
            print("API Test Passed: Received 200 OK")
            print("Response:", response.json())
        else:
            print(f"API Test Failed: Received {response.status_code}")
            print("Response:", response.json())
    except Exception as e:
        print(f"API Test Failed: An error occurred: {e}")

# Connect to the PostgreSQL database and list all employees, events
def test_database():
    try:
        # Setup database connection
        DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://abdelnasser:greatness@db:5432/mydatabase')
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Get all employees
        employees = session.query(Employee).all()
        print("Employees:")
        for employee in employees:
            print(employee)

        # Get the first 15 events
        events = session.query(Event).all()[:15]
        print("\nFirst 15 Events:")
        for event in events:
            print(event)

        # Get events for the employee with ID 1
        events_for_employee_1 = session.query(Event).filter_by(employee_id=1).all()
        print("\nEvents for Employee ID 1:")
        for event in events_for_employee_1:
            print(event)

        session.close()

    except Exception as e:
        print(f"Database Test Failed: An error occurred: {e}")

if __name__ == "__main__":
    print("Running Environment Variables Check...")
    print_env_variables()  # Print all environment variables

    print("Running API Test...")
    test_api()
    
    print("\nRunning Database Test...")
    test_database()
