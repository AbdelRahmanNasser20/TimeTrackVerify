from flask import Blueprint, jsonify, request
from datetime import datetime
from .extensions import db
from .db_queries import get_employee_id, count_entries_for_employee, sum_hours_by_role_from_db, get_events_for_employee_by_date
from .verify_timesheet import generate_report, process_timesheet_entries

api = Blueprint('api', __name__)

@api.route('/api/message')
def get_message():
    return jsonify(message="Hello from Flask!")

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
        print("Hello from Verify")
        data = request.get_json()
        # Check if the request payload contains the necessary fields
        if not data or 'tableData' not in data or 'email' not in data:
            print("400 bad error")
            return jsonify({'error': True, 'message': 'Invalid request payload'}), 400  # Bad Request
        
        
        # Check if email or timesheet entries are empty
        email = data["email"].lower()
        timeSheetEntries = data['tableData']        

        if not email:
            return jsonify({'error': True, 'message': 'Email is required'}), 422  # Unprocessable Entity

        if not timeSheetEntries:
            return jsonify({'error': True, 'message': 'Timesheet entries are required'}), 422  # Unprocessable Entity
                
        report,invalidEntries = {}, {}

        # Check if the email exists in the database
        employee_id = get_employee_id(email)
        print("employee_id: ", employee_id)
        
        if employee_id is None:
            return jsonify({'error': True, 'message': 'Email not found in the database'}), 404  # Not Found

        report = generate_report(employee_id, timeSheetEntries)
        print(report)
        report["emailFound"] = True

        invalidEntries = process_timesheet_entries(employee_id, timeSheetEntries)

        return jsonify({"report": report, "invalidEntries": invalidEntries}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': True, 'message': 'Internal Server Error'}), 500  # Internal Server Error


@api.route('/api/check_db_connection')
def check_db_connection():
    try:
        result = db.session.execute('SELECT 1').scalar()
        if result == 1:
            return jsonify(status='success', message='Database connection is working.')
        else:
            return jsonify(status='error', message='Database connection failed.')
    except Exception as e:
        return jsonify(status='error', message=str(e))