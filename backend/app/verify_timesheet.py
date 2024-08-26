from app.db_queries import retrieve_all_db_events_for_employee, get_events_for_employee_by_date, count_entries_for_employee, sum_hours_by_role_from_db
from datetime import datetime
from .extensions import db


class Event:
        def __init__(self, date, duration, position, location):
            self.date = date
            self.duration = duration
            self.position = position
            self.location = location

def reformat_date(date_str):
    """
    Reformats a date string from 'YYYY-MM-DD' to 'MM/DD/YYYY'.
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%m/%d/%Y')
    except ValueError:
        print(f"Invalid date format for {date_str}")
        return "Invalid date format"
    

def sum_hours_by_position_from_timesheet(timesheet_entries):
    """
    Sums up hours for each position from a list of timesheet entries.

    :param timesheet_entries: List of dictionaries containing timesheet data
    :return: Dictionary with the total hours summed up for each position
    """
    total_hours_by_position = {}

    for entry in timesheet_entries:
        position = entry['position']
        hours = float(entry['hours'])  # Convert hours to float for calculation

        if position in total_hours_by_position:
            total_hours_by_position[position] += hours
        else:
            total_hours_by_position[position] = hours

    print(f"Summed hours by position from timesheet: {total_hours_by_position}")
    return total_hours_by_position

def validate_entry(db_entry, timesheet_entry):
    """
    Validates an individual timesheet entry against a database entry.
    Returns a dictionary indicating the validation status for each field.
    """
    try:
        db_date, db_duration, db_position, db_location = db_entry.date, db_entry.duration, db_entry.position, db_entry.location
        timesheet_date = timesheet_entry['date']
        timesheet_duration = float(timesheet_entry['hours'])
        timesheet_location = timesheet_entry['location']
        timesheet_position = timesheet_entry['position']

        validation_status = {
            'date': db_date,
            'duration': timesheet_duration == float(db_duration),
            'location': True,
            'position': timesheet_position == db_position
        }
        print(f"Validated entry: {validation_status}")
        return validation_status
    except Exception as e:
        print(f"Error validating entry: {e}")
        return {'date': False, 'duration': False, 'location': False, 'position': False}


def process_timesheet_entries(db_entries, timesheet_entries):
    """
    Processes a list of timesheet entries against a list of database entries.
    """
    invalid_entries = []
    for entry in timesheet_entries:
        formatted_date = reformat_date(entry['date'])
        position = entry['position']
        matching_db_entry = None

        for db_entry in db_entries:
            if db_entry.date == formatted_date and db_entry.position == position:
                matching_db_entry = db_entry
                break

        if matching_db_entry:
            validation = validate_entry(matching_db_entry, entry)
            if not all(validation.values()):
                invalid_entries.append(validation)
        else:
            invalid_entries.append({
                'date': formatted_date,
                'duration': False,
                'position': False
            })

    print(f"Processed entries. Invalid entries: {invalid_entries}")
    return invalid_entries

def generate_report(db_entries, timesheet_entries):
    """
    Generates a report comparing timesheet entries to database entries.
    """
    try:
        report = {}
        report["numberOfTimesheetEntries"] = len(timesheet_entries)
        report["numberOfDatabaseEntries"] = len(db_entries)
        report["databaseHours"] = sum_hours_by_position_from_timesheet(db_entries)
        report["timesheetHours"] = sum_hours_by_position_from_timesheet(timesheet_entries)
        return report
    except Exception as e:
        print(f"Error generating report: {e}")
        return {}

def prepare_report_data(employee_id, timesheet_entries, session=db.session):
    """
    Prepares the data needed for generating the report.
    """
    db_entries = retrieve_all_db_events_for_employee(employee_id, session)
    return generate_report(db_entries, timesheet_entries)

# Example usage
if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))    
    from app import create_app

    app = create_app('development')

    with app.app_context():
        from app.db_queries import get_events_for_employee_by_date, sum_hours_by_role_from_db, count_entries_for_employee
        from datetime import datetime
                
    

        # Dummy database data
        dummy_db_events = {
            '2023-12-01': [
                Event('12/01/2023', 5.0, 'Teacher - Lead', 'School A'),
                Event('12/01/2023', 2.0, 'Teacher - Assistant', 'School A')
            ],
            '2023-12-02': [
                Event('12/02/2023', 3.0, 'Teacher - Assistant', 'School B'),
                Event('12/02/2023', 4.0, 'Teacher - Lead', 'School B')
            ]
        }
        
        
        timesheet_entries = [
            {"date": '12/01/2023', "hours": 5.0, "position": 'Teacher - Lead', "location": 'School A'},
            {"date": '12/01/2023', "hours": 2.0, "position": 'Teacher - Assistant', "location": 'School A'},
            {"date": '12/02/2023', "hours": 3.0, "position": 'Teacher - Assistant', "location": 'School B'},
            {"date": '12/02/2023', "hours": 4.0, "position": 'Teacher - Lead', "location": 'School B'}
        ]
        
            # Generate and print the report
        report = generate_report(1, timesheet_entries)
        print(report)
        
        # Process and print invalid entries
        invalid_entries = process_timesheet_entries(1, timesheet_entries)
        print(f"Invalid Entries: {invalid_entries}")
