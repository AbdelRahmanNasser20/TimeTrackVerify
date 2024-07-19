from .db_queries import get_events_for_employee_by_date, sum_hours_by_role_from_db, count_entries_for_employee
from datetime import datetime

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

def process_timesheet_entries(employee_id, timesheet_entries):
    """
    Processes a list of timesheet entries for a given employee.
    Validates each timesheet entry against the corresponding database entry.
    """
    invalid_entries = []

    for timesheet_entry in timesheet_entries:
        date, position, hours, location = reformat_date(timesheet_entry['date']), timesheet_entry['position'], timesheet_entry['hours'], timesheet_entry['location']
        db_entry = get_events_for_employee_by_date(employee_id, date)

        if db_entry:
            validation = validate_entry(db_entry, timesheet_entry)
            if not all(validation.values()):
                invalid_entries.append(validation)
        else:
            # No matching database entry found
            invalid_entries.append({'date': date, 'duration': False, 'location': False, 'position': False})

    print(f"Processed entries. Invalid entries: {invalid_entries}")
    return invalid_entries

def generate_report(employee_id, timesheet_entries):
    """
    Generates a report comparing timesheet entries to database entries.
    """
    try:
        report = {}
        report["timesheetEntries"] = len(timesheet_entries)
        report["databaseEntries"] = count_entries_for_employee(employee_id)
        
        report["databaseHours"] = sum_hours_by_role_from_db(employee_id)
        report["timesheetHours"] = sum_hours_by_position_from_timesheet(timesheet_entries)
        
        print(f"Generated report: {report}")
        return report
    except Exception as e:
        print(f"Error generating report: {e}")
        return {}

# Example usage
if __name__ == "__main__":
    employee_id = 1  # Replace with actual employee ID for testing
    timesheet_entries = [
        {'date': '2023-12-01', 'position': 'Teacher - Lead', 'hours': 5.0, 'location': 'School A'},
        {'date': '2023-12-02', 'position': 'Teacher - Assistant', 'hours': 3.0, 'location': 'School B'}
    ]
    
    report = generate_report(employee_id, timesheet_entries)
    print(report)
