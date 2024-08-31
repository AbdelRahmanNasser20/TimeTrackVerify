from .models import Event
from .extensions import db
from datetime import datetime
from .db_queries import get_events_by_date, get_events_for_month


def sum_hours_by_role(events):
    """
    Fetches all entries for a given employee from the database and sums up the hours for each role.
    """
    total_hours_by_role = {}
            
    for event in events:        
        role = event["position"]
        hours = float(event["hours"])  # Ensure hours is a float

        if role in total_hours_by_role:
            total_hours_by_role[role] += hours
        else:
            total_hours_by_role[role] = hours        
    
    return total_hours_by_role

def validate_timesheet_entry_against_db( employee_id, entry, session=db.session):
    """
    Validates an individual timesheet entry against the database with partial matching.

    :param employee_id: The ID of the employee.
    :param timesheet_entry: A dictionary containing timesheet data.
    :return: A dictionary indicating the validation status for each field.
    """
    db_entries = get_events_by_date(employee_id, entry['date'],session=session)

    invalid_entry = {  
        'date': False,
        'hours': False,
        'position': False,
        'location': True
    }

    if not db_entries:
        return invalid_entry

    closest_match = None
    highest_match_count = 0

    for db_entry in db_entries:        
        # print("COMPARING THE TWO: ", entry['date'], db_entry["date"], entry['date'] ==  db_entry["date"] , type(entry['date']), type(db_entry['date']))        
        match = {
            'date': entry['date'] == db_entry['date'],
            'hours': entry['hours'] == db_entry["hours"],
            'position': entry['position'] == db_entry["position"],
            'location': True
        }
                        
        match_count = sum(match.values()) # Count how many fields matched

        if all(match.values()):            
            return match  # Exact match found

        if match_count > highest_match_count:
            closest_match = match
            highest_match_count = match_count

    return closest_match if closest_match else invalid_entry

def generate_report(employee_id, timesheet_entries, session=db.session):
    """
    Generates a report comparing timesheet entries to database entries with detailed feedback.

    :param employee_id: The ID of the employee.
    :param timesheet_entries: A list of dictionaries containing timesheet data.
    :return: A report dictionary containing the results of the comparison.
    """
    # invalid_entries = process_timesheet_entries(employee_id, timesheet_entries)
    # print("GENERATING REPORT ", employee_id, timesheet_entries)
    
    if not timesheet_entries:
        return {
            "numberOfTimesheetEntries": 0,
            "numberOfDatabaseEntries": 0,
            "invalidEntries": [],
            "databaseHours": {},
            "timesheetHours": {}
        }
    
    invalid_entries = []
    
    db_entries = get_events_for_month(employee_id, (timesheet_entries[0]['date']),session)
    
    database_roles_by_hours = sum_hours_by_role(db_entries)
    timesheet_roles_by_hours = sum_hours_by_role(timesheet_entries)

    print("db_entries ", db_entries)
    print("Comparing " , db_entries)
    print("To " , timesheet_entries)
    for entry in timesheet_entries:
        validation = validate_timesheet_entry_against_db(employee_id, entry,session)
        # print("THIS IS : ", not all(validation.values()), all(validation.values()), validation)
        # if invalid entry
        if not all(validation.values()):
            print("INVALID ENTRY: ", validation)
            # Change valdaition schema to include the date in the report
            validation["date"] = entry["date"]            
            invalid_entries.append(validation)


    # print("Invalid entries: ", invalid_entries)
    #  iterate through each entry    
    report = {            
        "numberOfTimesheetEntries": len(timesheet_entries),
        "numberOfDatabaseEntries": len(db_entries),
        "invalidEntries": invalid_entries,
        "databaseHours": database_roles_by_hours,
        "timesheetHours": timesheet_roles_by_hours
    }

    return report


if __name__ == "__main__":
    employee_id = 1  # Example employee ID
    timesheet_entries = [
        {"date": "12/03/2023", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"},
        {"date": "12/04/2023", "hours": 2.00, "position": "Teacher - Lead", "location": "Oakland Terrace ES"},
        {"date": "12/05/2023", "hours": 2.75, "position": "Teacher - Assistant", "location": "Burning Tree ES"},
        {"date": "12/06/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"},
        {"date": "12/11/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "ST Andrew"},
        {"date": "12/13/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"},
        {"date": "12/18/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "ST Andrew"},
        {"date": "12/20/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"}
        ]

    report = generate_report(employee_id, timesheet_entries)
    print(report)