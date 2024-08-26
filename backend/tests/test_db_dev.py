# import os
# import pytest
# from flask import Flask
# from app import create_app
# from app.extensions import db
# from app.routes import api
# import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# @pytest.fixture
# def client():
#     # Create a test Flask application with the production configuration
#     app = create_app('production')
    
#     # Override the DEBUG setting if necessary
#     app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'

#     assert app.config['SQLALCHEMY_DATABASE_URI'] ==  os.getenv('HEROKU_DATABASE_URL'), "Using inccorret db"
#     print("USING THIS , " ,  app.config['SQLALCHEMY_DATABASE_URI'])

#     # Use the HEROKU_DATABASE_URL if set, otherwise fallback to default
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_DATABASE_URL', 'postgresql://abdelnasser:greatness@localhost:5432/mydatabase')
    
#     # Initialize the SQLAlchemy object with the app
#     db.init_app(app)
    
#     # Register your Blueprint
#     app.register_blueprint(api)
    
#     # Use the test client to make requests to the app
#     with app.test_client() as client:
#         with app.app_context():
#             yield client

# def test_check_db_connection(client):
#     response = client.get('/run_all_checks')
#     assert response.status_code == 200
#     data = response.get_json()
    
#     # Verify that the DB connection check passed
#     assert any(result['check_db_connection'] == 'success' for result in data), "DB Connection Failed"

# def test_list_tables(client):
#     response = client.get('/run_all_checks')
#     assert response.status_code == 200
#     data = response.get_json()
    
#     # Extract the list of tables from the response
#     tables = next((result['tables'] for result in data if 'tables' in result), None)
#     assert tables is not None, "No tables were listed in the response"
    
#     # Define the expected tables
#     expected_tables = {"alembic_version", "user", "events", "employees"}
    
#     # Verify that all expected tables are present
#     missing_tables = expected_tables - set(tables)
#     assert not missing_tables, f"Missing tables: {missing_tables}"

# def test_check_table_employees(client):
#     response = client.get('/run_all_checks')
#     assert response.status_code == 200
#     data = response.get_json()
    
#     # Verify that the 'employees' table exists
#     assert any('check_table_employees' in result and result['check_table_employees'] == 'success' for result in data), "Employees Table Check Failed"

# def test_get_employees(client):
#     response = client.get('/run_all_checks')
#     assert response.status_code == 200
#     data = response.get_json()

#     # Verify that we can retrieve employees
#     employees = next((result['employees'] for result in data if 'employees' in result), None)
#     assert employees is not None, "No employees were retrieved"
#     assert len(employees) == 10, "The number of employees retrieved is not equal to 10"

#     # Optionally, you can check the content of the employees
#     expected_employee_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
#     retrieved_employee_ids = {int(list(employee.keys())[0]) for employee in employees}
#     assert expected_employee_ids == retrieved_employee_ids, "The retrieved employees do not match the expected ones"
