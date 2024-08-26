from datetime import datetime

# Dummy Event class
class Event:
    def __init__(self, timestamp, duration, position, location):
        self.timestamp = timestamp
        self.duration = duration
        self.position = position
        self.location = location

# Dummy database data
dummy_db_events = {
    '2023-12-01 08:00:00': [
        Event('2023-12-01 08:00:00', 5.0, 'Teacher - Lead', 'School A'),
        Event('2023-12-01 09:00:00', 2.0, 'Teacher - Assistant', 'School A')
    ],
    '2023-12-02 10:00:00': [
        Event('2023-12-02 10:00:00', 3.0, 'Teacher - Assistant', 'School B'),
        Event('2023-12-02 12:00:00', 4.0, 'Teacher - Lead', 'School B')
    ]
}

# Helper functions
def reformat_timestamp(date_str):
    """
    Reformats a timestamp string from 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' to 'YYYY-MM-DD HH:MM:SS'.
    """
    try:
        if len(date_str) == 10:  # If the date_str is 'YYYY-MM-DD'
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
        else:  # If the date_str is 'YYYY-MM-DD HH:MM:SS'
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        print(f"Invalid timestamp format for {date_str}")
        return "Invalid timestamp format"

def get_events_for_employee_by_date(employee_id, timestamp):
    """
    Fetches all events from the dummy database for a given employee on a specific date.
    """
    try:
        events = dummy_db_events.get(timestamp.split()[0] + ' 00:00:00', [])
        if events:
            print(f"Found {len(events)} events for employee ID {employee_id} on date {timestamp}")
        else:
            print(f"No events found for employee ID {employee_id} on date {timestamp}")
        return events
    except Exception as e:
        print(f"Error retrieving events for employee ID {employee_id} on date {timestamp}: {e}")
        return []

def sum_hours_by_role_from_db(employee_id):
    """
    Sums hours for each role from the dummy database.
    """
    total_hours_by_role = {}
    
    for date, events in dummy_db_events.items():
        for event in events:
            position = event.position
            hours = event.duration
            if position in total_hours_by_role:
                total_hours_by_role[position] += hours
            else:
                total_hours_by_role[position] = hours
    
    print(f"Summed hours by role from database: {total_hours_by_role}")
    return total_hours_by_role

def count_entries_for_employee(employee_id):
    """
    Counts the total number of entries for the employee in the dummy database.
    """
    total_entries = sum(len(events) for events in dummy_db_events.values())
    print(f"Total database entries for employee {employee_id}: {total_entries}")
    return total_entries

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

def validate_entry(db_entries, timesheet_entry):
    """
    Validates an individual timesheet entry against a list of database entries.
    Returns a dictionary indicating the validation status for each field.
    """
    try:
        validation_status_list = []

        timesheet_timestamp = reformat_timestamp(timesheet_entry['date'])
        timesheet_duration = float(timesheet_entry['hours'])
        timesheet_location = timesheet_entry['location']
        timesheet_position = timesheet_entry['position']

        for db_entry in db_entries:
            db_timestamp, db_duration, db_position, db_location = db_entry.timestamp, db_entry.duration, db_entry.position, db_entry.location
            validation_status = {
                'timestamp': db_timestamp,
                'duration': timesheet_duration == float(db_duration),
                'location': timesheet_location == db_location,
                'position': timesheet_position == db_position
            }
            validation_status_list.append(validation_status)

        print(f"Validated entries: {validation_status_list}")
        return validation_status_list
    except Exception as e:
        print(f"Error validating entry: {e}")
        return [{'timestamp': False, 'duration': False, 'location': False, 'position': False}]

def process_timesheet_entries(employee_id, timesheet_entries):
    """
    Processes a list of timesheet entries for a given employee.
    Validates each timesheet entry against the corresponding database entry.
    """
    invalid_entries = []

    for timesheet_entry in timesheet_entries:
        timestamp = reformat_timestamp(timesheet_entry['date'])  # Reformat to 'YYYY-MM-DD HH:MM:SS'
        position, hours, location = timesheet_entry['position'], timesheet_entry['hours'], timesheet_entry['location']
        
        db_entries = get_events_for_employee_by_date(employee_id, timestamp)

        if db_entries:
            validations = validate_entry(db_entries, timesheet_entry)
            for validation in validations:
                if not all(validation.values()):
                    invalid_entries.append(validation)
        else:
            # No matching database entry found
            invalid_entries.append({'timestamp': timestamp, 'duration': False, 'location': False, 'position': False})

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

# Test cases
def run_tests():
    employee_id = 1  # Mock employee ID for testing

    # Case 1: Perfect match
    timesheet_entries_1 = [
        {'date': '2023-12-01 08:00:00', 'position': 'Teacher - Lead', 'hours': 5.0, 'location': 'School A'},
        {'date': '2023-12-01 09:00:00', 'position': 'Teacher - Assistant', 'hours': 2.0, 'location': 'School A'},
        {'date': '2023-12-02 10:00:00', 'position': 'Teacher - Assistant', 'hours': 3.0, 'location': 'School B'},
        {'date': '2023-12-02 12:00:00', 'position': 'Teacher - Lead', 'hours': 4.0, 'location': 'School B'}
    ]
    report_1 = generate_report(employee_id, timesheet_entries_1)
    invalid_entries_1 = process_timesheet_entries(employee_id, timesheet_entries_1)
    assert report_1["timesheetEntries"] == 4
    assert report_1["databaseEntries"] == 4
    assert report_1["databaseHours"] == {'Teacher - Lead': 9.0, 'Teacher - Assistant': 5.0}
    assert report_1["timesheetHours"] == {'Teacher - Lead': 9.0, 'Teacher - Assistant': 5.0}
    assert len(invalid_entries_1) == 0

    # Case 2: Mismatched hours
    timesheet_entries_2 = [
        {'date': '2023-12-01 08:00:00', 'position': 'Teacher - Lead', 'hours': 6.0, 'location': 'School A'},  # Mismatch in hours
        {'date': '2023-12-01 09:00:00', 'position': 'Teacher - Assistant', 'hours': 2.0, 'location': 'School A'},
        {'date': '2023-12-02 10:00:00', 'position': 'Teacher - Assistant', 'hours': 3.0, 'location': 'School B'},
        {'date': '2023-12-02 12:00:00', 'position': 'Teacher - Lead', 'hours': 4.0, 'location': 'School B'}
    ]
    report_2 = generate_report(employee_id, timesheet_entries_2)
    invalid_entries_2 = process_timesheet_entries(employee_id, timesheet_entries_2)
    assert report_2["timesheetEntries"] == 4
    assert len(invalid_entries_2) == 1  # Should detect one invalid entry
    assert invalid_entries_2[0]['duration'] == False

    # Case 3: Mismatched location
    timesheet_entries_3 = [
        {'date': '2023-12-01 08:00:00', 'position': 'Teacher - Lead', 'hours': 5.0, 'location': 'School B'},  # Mismatch in location
        {'date': '2023-12-01 09:00:00', 'position': 'Teacher - Assistant', 'hours': 2.0, 'location': 'School A'},
        {'date': '2023-12-02 10:00:00', 'position': 'Teacher - Assistant', 'hours': 3.0, 'location': 'School B'},
        {'date': '2023-12-02 12:00:00', 'position': 'Teacher - Lead', 'hours': 4.0, 'location': 'School B'}
    ]
    report_3 = generate_report(employee_id, timesheet_entries_3)
    invalid_entries_3 = process_timesheet_entries(employee_id, timesheet_entries_3)
    assert report_3["timesheetEntries"] == 4
    assert len(invalid_entries_3) == 1  # Should detect one invalid entry
    assert invalid_entries_3[0]['location'] == False

    # Case 4: Extra entry in timesheet (no corresponding database entry)
    timesheet_entries_4 = [
        {'date': '2023-12-01 08:00:00', 'position': 'Teacher - Lead', 'hours': 5.0, 'location': 'School A'},
        {'date': '2023-12-01 09:00:00', 'position': 'Teacher - Assistant', 'hours': 2.0, 'location': 'School A'},
        {'date': '2023-12-02 10:00:00', 'position': 'Teacher - Assistant', 'hours': 3.0, 'location': 'School B'},
        {'date': '2023-12-02 12:00:00', 'position': 'Teacher - Lead', 'hours': 4.0, 'location': 'School B'},
        {'date': '2023-12-02 14:00:00', 'position': 'Teacher - Assistant', 'hours': 1.0, 'location': 'School C'}  # Extra entry
    ]
    report_4 = generate_report(employee_id, timesheet_entries_4)
    invalid_entries_4 = process_timesheet_entries(employee_id, timesheet_entries_4)
    assert report_4["timesheetEntries"] == 5
    assert len(invalid_entries_4) == 1  # Should detect one invalid entry for missing database entry
    assert invalid_entries_4[0]['position'] == False

    # Case 5: No entries for a date in the database
    timesheet_entries_5 = [
        {'date': '2023-12-01 08:00:00', 'position': 'Teacher - Lead', 'hours': 5.0, 'location': 'School A'},
        {'date': '2023-12-01 09:00:00', 'position': 'Teacher - Assistant', 'hours': 2.0, 'location': 'School A'},
        {'date': '2023-12-03 08:00:00', 'position': 'Teacher - Assistant', 'hours': 3.0, 'location': 'School B'},  # Date not in DB
        {'date': '2023-12-02 12:00:00', 'position': 'Teacher - Lead', 'hours': 4.0, 'location': 'School B'}
    ]
    report_5 = generate_report(employee_id, timesheet_entries_5)
    invalid_entries_5 = process_timesheet_entries(employee_id, timesheet_entries_5)
    assert report_5["timesheetEntries"] == 4
    assert len(invalid_entries_5) == 1  # Should detect one invalid entry for the date mismatch
    assert invalid_entries_5[0]['timestamp'] == '2023-12-03 00:00:00'

    print("All test cases passed!")

if __name__ == "__main__":
    run_tests()

