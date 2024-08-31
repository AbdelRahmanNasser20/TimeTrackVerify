import pytest
from app.models import Employee, Event
from app.extensions import db
from app.db_queries import get_employee_id, count_entries_for_employee, sum_hours_by_role_from_db, get_events_for_employee_by_date, get_events_for_month
from app.new_validate_timesheet import generate_report

def test_get_employee_id(session):
    """Test retrieving an employee ID by email."""
    email = "abdel.nasser045@gmail.com"
    employee_id = get_employee_id(email, session)
    if employee_id:
        print(f"Success: Found employee ID {employee_id} for email {email}")
    else:
        print(f"Failed: No employee found for email {email}")

def test_count_entries_for_employee(session):
    """Test counting the number of entries for a given employee ID."""
    email = "abdel.nasser045@gmail.com"
    employee_id = get_employee_id(email)
    if employee_id:
        count = count_entries_for_employee(employee_id,session)
        assert count == 8 , "Failed to count entries"
        print(f"Success: Counted {count} entries for employee ID {employee_id}")
    else:
        print(f"Failed: Could not count entries because no employee ID was found for email {email}")

def test_sum_hours_by_role_from_db(session):
    """Test summing hours by role for a given employee."""
    email = "abdel.nasser045@gmail.com"
    employee_id = get_employee_id(email,session)
    if employee_id:
        total_hours_by_role = sum_hours_by_role_from_db(employee_id)
        assert total_hours_by_role == {'Teacher - Lead': 16.75, 'Teacher - Assistant': 2.75}
        print(f"Success: Summed hours by role for employee ID {employee_id}: {total_hours_by_role}")
    else:
        print(f"Failed: Could not sum hours by role because no employee ID was found for email {email}")

def test_get_events_for_employee_by_date(session):
    """Test retrieving events for an employee on a specific date."""
    email = "abdel.nasser045@gmail.com"
    date = "2023-12-06"  # Use the appropriate date format and value
    employee_id = get_employee_id(email,session)
    if employee_id:
        events = get_events_for_employee_by_date(employee_id, date)
        assert len(events) == 1, f"Expected 1 event but got {len(events)}"
        if events:
            print(f"Success: Found {len(events)} events for employee ID {employee_id} on date {date}")            
        else:
            print(f"No events found for employee ID {employee_id} on date {date}")
    else:
        print(f"Failed: Could not retrieve events because no employee ID was found for email {email}")

# def test_invalid_events(session):
#     """Test retrieving events for an employee on a specific date."""
#     email = "abdel.nasser045@gmail.com"    
#     employee_id = get_employee_id(email,session)
    
#     if not employee_id:
#         print(f"Failed: Could not retrieve events because no employee ID was found for email {email}")
#         assert False
    
#     db_entries = get_events_for_month(employee_id, "12/01/2023",session)
    
#     timesheet_entries = [
#     {"date": "12/03/2023", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"},
#     {"date": "12/04/2023", "hours": 2.00, "position": "Teacher - Lead", "location": "Oakland Terrace ES"},
#     {"date": "12/05/2023", "hours": 2.75, "position": "Teacher - Assistant", "location": "Burning Tree ES"},
#     {"date": "12/06/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"},
#     {"date": "12/11/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "ST Andrew"},
#     {"date": "12/13/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"},
#     {"date": "12/18/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "ST Andrew"},
#     {"date": "12/20/2023", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"}
# ]
    
#     invalid_events = generate_report(db_entries,timesheet_entries)["invalidEntries"]
#     assert invalid_events == [], f"Expected 0 invalid events but got {len(invalid_events)}"
        
    