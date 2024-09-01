from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import text
from .extensions import db
from .db_queries import get_employee_id, retrieve_all_db_events_for_employee
# from .verify_timesheet import prepare_report_data, process_timesheet_entries
from .new_validate_timesheet import generate_report
import os

api = Blueprint('api', __name__)

@api.route('/api/message')
def get_message():
    return jsonify(message="Hello from Flask!")



@api.route('/api/check_db_connection')
def db_connection():
    return jsonify(message="Hello from Flask!", status = "success", status_code = 200)

@api.route('/api/time')
def get_time():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(time=current_time)

@api.route('/api/status')
def get_status():
    return jsonify(status="Everything is running smoothly!")


@api.route('/verify', methods=['POST'])
def verify_timesheet():
    try:
        
        data = request.get_json()
        print(f"Received data")

        if not data or 'tableData' not in data or 'email' not in data:
            return jsonify({'error': True, 'message': 'Invalid request payload'}), 400
        
        email = data["email"].lower()
        timesheet_entries = data['tableData']

        if not email:
            return jsonify({'error': True, 'message': 'Email is required'}), 422

        if not timesheet_entries:
            return jsonify({'error': True, 'message': 'Timesheet entries are required'}), 422
        
        employee_id = get_employee_id(email)
        
        if employee_id is None:
            return jsonify({'error': True, 'message': 'Email not found in the database'}), 403        

        print("Generating report", timesheet_entries)
        report = generate_report(employee_id, timesheet_entries)        

        print(f"Generated report: {report}")
        report["emailFound"] = True

        return jsonify({"report": report}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': True, 'message': 'Internal Server Error'}), 500

@api.route('/run_all_checks')
def run_all_checks():
    print("RETRIVING DB URL ", os.getenv('DATABASE_URL'))
    print(f"Current SQLAlchemy Database URI: {db.engine.url}")
    results = []
    
    # Check DB Connection
    try:
        result = db.session.execute(text('SELECT 1')).scalar()
        if result == 1:
            results.append({'check_db_connection': 'success'})
        else:
            results.append({'check_db_connection': 'failed'})
    except Exception as e:
        results.append({'check_db_connection': str(e)})

    # List Tables and Verify Their Presence
    expected_tables = {"alembic_version", "user", "events", "employees"}
    try:
        result = db.session.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")).fetchall()
        tables = {row[0] for row in result}  # Use a set for easier comparison
        
        missing_tables = expected_tables - tables
        if not missing_tables:
            results.append({'list_tables': 'success', 'tables': list(tables)})
        else:
            results.append({'list_tables': 'failed', 'missing_tables': list(missing_tables)})
    except Exception as e:
        results.append({'list_tables': str(e)})

    # Check if 'employees' Table Exists
    try:
        result = db.session.execute(text("SELECT to_regclass('employees')")).scalar()
        if result:
            results.append({'check_table_employees': 'success'})
        else:
            results.append({'check_table_employees': 'failed'})
    except Exception as e:
        results.append({'check_table_employees': str(e)})

    # Get All Rows from 'employees' Table (First 10)
    try:
        result = db.session.execute(text("SELECT id, name FROM employees ORDER BY id LIMIT 10")).fetchall()
        employees = [{str(id): name} for id, name in result]
        results.append({'get_employees': 'success', 'employees': employees})
    except Exception as e:
        results.append({'get_employees': str(e)})

    return jsonify(results)
