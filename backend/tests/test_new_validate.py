import pytest
from app.db_queries import get_events_by_date
from app.models import Employee, Event
from datetime import datetime

from app.new_validate_timesheet import  sum_hours_by_role, generate_report,validate_timesheet_entry_against_db

# def test_yyyy_mm_dd_to_mm_dd_yyyy():
#     # Test converting from 'YYYY-MM-DD' to 'MM/DD/YYYY'
#     assert reformat_date('2024-08-28') == '08/28/2024'
#     assert reformat_date('1999-12-31') == '12/31/1999'
#     assert reformat_date('2000-01-01') == '01/01/2000'

# def test_mm_dd_yyyy_to_yyyy_mm_dd():
#     # Test converting from 'MM/DD/YYYY' to 'YYYY-MM-DD'
#     assert reformat_date('08/28/2024') == '2024-08-28'
#     assert reformat_date('12/31/1999') == '1999-12-31'
#     assert reformat_date('01/01/2000') == '2000-01-01'

# def test_invalid_date_format():
#     # Test handling of invalid date formats
#     assert reformat_date('28-08-2024') == 'Invalid date format'
#     assert reformat_date('2024/08/28') == 'Invalid date format'
#     assert reformat_date('08-28-2024') == 'Invalid date format'
#     assert reformat_date('2024-31-12') == 'Invalid date format'
#     assert reformat_date('12/31/99') == 'Invalid date format'

# def test_unknown_format():
#     # Test handling of unknown date format
#     assert reformat_date('20240828') == 'Unknown date format'
#     assert reformat_date('08282024') == 'Unknown date format'

from datetime import datetime

def test_sum_hours_by_role():
    timesheet_entries = [
        {"date": "2023-12-03", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"},
        {"date": "2023-12-04", "hours": 2.00, "position": "Teacher - Lead", "location": "Oakland Terrace ES"},
        {"date": "2023-12-05", "hours": 2.75, "position": "Teacher - Assistant", "location": "Burning Tree ES"},
        {"date": "2023-12-06", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"},
        {"date": "2023-12-11", "hours": 2.50, "position": "Teacher - Lead", "location": "ST Andrew"},
        {"date": "2023-12-13", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"},
        {"date": "2023-12-18", "hours": 2.50, "position": "Teacher - Lead", "location": "ST Andrew"},
        {"date": "2023-12-20", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"}
    ]

    result = sum_hours_by_role(timesheet_entries)
    
    expected_result = {
        "Teacher - Lead": 16.75,
        "Teacher - Assistant": 2.75
    }
    
    assert result == expected_result, f"Failed: Expected {expected_result}, but got {result}"
    print("Success: sum_hours_by_role works as expected.")

def test_validate_timesheet_entry_against_db_single_event(session):
    employee = Employee(name="Test User", email="test.email@example.com")
    session.add(employee)
    session.commit()

    date = datetime.strptime('2023-12-03', '%Y-%m-%d')
    event = Event(
        date=date,
        hours=2.25,
        position="Teacher - Lead",
        location="Good Shepherd",
        employee_id=employee.id,
        name="Teaching Session"
    )    
    
    session.add(event)
    session.commit()

    entry = {"date": "2023-12-03", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"}
    validation = validate_timesheet_entry_against_db(employee.id, entry, session)

    expected_validation = {
        "date": True,
        "hours": True,
        "position": True,
        "location": True
    }
    
    assert validation == expected_validation, f"Failed: Expected {expected_validation}, but got {validation}"
    print("Success: validate_timesheet_entry_against_db works as expected.")

def test_validate_timesheet_entry_against_db_invalid_hours(session):
    employee = Employee(name="Test User", email="test.email@example.com")
    session.add(employee)
    session.commit()

    date = datetime.strptime('2023-12-03', '%Y-%m-%d')
    event = Event(
        date=date,
        hours=2.25,
        position="Teacher - Lead",
        location="Good Shepherd",
        employee_id=employee.id,
        name="Teaching Session"
    )
    
    session.add(event)
    session.commit()

    entry = {"date": "2023-12-03", "hours": 3.00, "position": "Teacher - Lead", "location": "Good Shepherd"}
    validation = validate_timesheet_entry_against_db(employee.id, entry, session)    

    expected_validation = {
        "date": True,
        "hours": False,
        "position": True,
        "location": True
    }

    assert validation == expected_validation, f"Failed: Expected {expected_validation}, but got {validation}"
    print("Success: validate_timesheet_entry_against_db correctly identifies hours mismatch.")

def test_validate_timesheet_entry_against_db_closest_match_all_events_invalid(session):
    employee = Employee(name="Test User", email="test.email@example.com")
    session.add(employee)
    session.commit()

    date = datetime.strptime('2023-12-03', '%Y-%m-%d')

    event1 = Event(
        date=date,
        hours=3,
        position="Teacher - Lead",
        location="Good Shepherd",
        employee_id=employee.id,
        name="Teaching Session"
    )
    
    event2 = Event(
        date=date,
        hours=3.00,
        position="Teacher - Assistant",
        location="Good Shepherd",
        employee_id=employee.id,
        name="Teaching Session"
    )
    
    session.add_all([event1, event2])
    session.commit()

    entry = {"date": "2023-12-03", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"}
    validation = validate_timesheet_entry_against_db(employee.id, entry, session)

    expected_validation = {
        "date": True,
        "hours": False,
        "position": True,
        "location": True
    }

    assert validation == expected_validation, f"Failed: Expected {expected_validation}, but got {validation}"
    print("Success: validate_timesheet_entry_against_db correctly identifies the closest match among multiple events.")

def test_generate_report_employee_abdel(session):

    timesheet_entries = [
        {"date": "2023-12-03", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"},
        {"date": "2023-12-04", "hours": 2.00, "position": "Teacher - Lead", "location": "Oakland Terrace ES"},
        {"date": "2023-12-05", "hours": 2.75, "position": "Teacher - Assistant", "location": "Burning Tree ES"},
        {"date": "2023-12-06", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"},
        {"date": "2023-12-11", "hours": 2.50, "position": "Teacher - Lead", "location": "ST Andrew"},
        {"date": "2023-12-13", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"},
        {"date": "2023-12-18", "hours": 2.50, "position": "Teacher - Lead", "location": "ST Andrew"},
        {"date": "2023-12-20", "hours": 2.50, "position": "Teacher - Lead", "location": "Forest Knolls ES"}
    ]

    report = generate_report(1, timesheet_entries, session)
    
    expected_report = {
        "numberOfTimesheetEntries": 8,
        "numberOfDatabaseEntries": 8, 
        "invalidEntries": [],
        "databaseHours": {
            "Teacher - Lead": 16.75,
            "Teacher - Assistant": 2.75
        },
        "timesheetHours": {
            "Teacher - Lead": 16.75,
            "Teacher - Assistant": 2.75
        }
    }
    
    assert report["numberOfTimesheetEntries"] == expected_report["numberOfTimesheetEntries"], \
        f"Failed: Expected {expected_report['numberOfTimesheetEntries']} timesheet entries, but got {report['numberOfTimesheetEntries']}"
    assert report["numberOfDatabaseEntries"] == expected_report["numberOfDatabaseEntries"], \
        f"Failed: Expected {expected_report['numberOfDatabaseEntries']} invalid entries, but got {report['numberOfDatabaseEntries']}"
    
    assert report["invalidEntries"] == expected_report["invalidEntries"], \
        f"Failed: Expected invalid entries {expected_report['invalidEntries']}, but got {report['invalidEntries']}"

    assert report["databaseHours"] == expected_report["databaseHours"], \
        f"Failed: Expected database hours {expected_report['databaseHours']}, but got {report['databaseHours']}"
    assert report["timesheetHours"] == expected_report["timesheetHours"], \
        f"Failed: Expected timesheet hours {expected_report['timesheetHours']}, but got {report['timesheetHours']}"
    
    print("Success: generate_report works as expected.")

def test_generate_report_single_entry_invalid_hours(session):
    employee = Employee(name="Test User", email="test.email@example.com")
    session.add(employee)
    session.commit()

    date = datetime.strptime('2023-12-03', '%Y-%m-%d')
    event1 = Event(
        date=date,
        hours=2.25,
        position="Teacher - Lead",
        location="Good Shepherd",
        employee_id=employee.id,
        name="Teaching Session"
    )    
    
    session.add(event1)
    session.commit()

    entry = [{"date": "2023-12-03", "hours": 99, "position": "Teacher - Lead", "location": "Good Shepherd"}]
    report = generate_report(employee.id, entry, session)
    
    expected_report = {
        "numberOfTimesheetEntries": 1,
        "numberOfDatabaseEntries": 1, 
        "invalidEntries": [            
            {"date" : "2023-12-03", "hours": False, "position": True, "location": True }            
        ],
        "databaseHours": {
            "Teacher - Lead": 2.25,
        },
        "timesheetHours": {
            "Teacher - Lead": 99,
        }
    }
    
    assert report["numberOfTimesheetEntries"] == expected_report["numberOfTimesheetEntries"], \
        f"Failed: Expected {expected_report['numberOfTimesheetEntries']} timesheet entries, but got {report['numberOfTimesheetEntries']}"
    assert report["numberOfDatabaseEntries"] == expected_report["numberOfDatabaseEntries"], \
        f"Failed: Expected {expected_report['numberOfDatabaseEntries']} invalid entries, but got {report['numberOfDatabaseEntries']}"
    
    assert report["invalidEntries"] == expected_report["invalidEntries"], \
        f"Failed: Expected invalid entries {expected_report['invalidEntries']}, but got {report['invalidEntries']}"

    assert report["databaseHours"] == expected_report["databaseHours"], \
        f"Failed: Expected database hours {expected_report['databaseHours']}, but got {report['databaseHours']}"
    assert report["timesheetHours"] == expected_report["timesheetHours"], \
        f"Failed: Expected timesheet hours {expected_report['timesheetHours']}, but got {report['timesheetHours']}"
    
    print("Success: generate_report works as expected.")

def test_generate_report_single_entry_all_invalid_events(session):
    employee = Employee(name="Test User", email="test.email@example.com")
    session.add(employee)
    session.commit()

    event1 = Event(
        date="2023-12-03",
        hours=2,
        position="Teacher - Lead",
        location="Good Shepherd",
        employee_id=employee.id,
        name="Teaching Session"
    )                
        
    session.add(event1)
    session.commit()

    entry = [{"date": "2023-12-03", "hours": 1, "position": "Teacher - Lead", "location": "Good Shepherd"},
             {"date": "2023-12-11", "hours": 0, "position": "Teacher - Lead", "location": "False"},
             {"date": "2023-12-12", "hours": 0, "position": "Teacher - Lead", "location": "False"},
             {"date": "2023-12-13", "hours": 0, "position": "Teacher - Lead", "location": "False"}
    ]
    
    report = generate_report(employee.id, entry, session)
    
    expected_report = {
        "numberOfTimesheetEntries": 4,
        "numberOfDatabaseEntries": 1, 
        "invalidEntries": [                        
            {"date" : "2023-12-03", "hours": False, "position": True, "location": True },
            {"date" : "2023-12-11", "hours": False, "position": False, "location": True },
            {"date" : "2023-12-12", "hours": False, "position": False, "location": True },
            {"date" : "2023-12-13", "hours": False, "position": False, "location": True }            
        ],
        "databaseHours": {
            "Teacher - Lead": 2,
        },
        "timesheetHours": {            
            "Teacher - Lead": 1
        }
    }
    
    assert report["numberOfTimesheetEntries"] == expected_report["numberOfTimesheetEntries"], \
        f"Failed: Expected {expected_report['numberOfTimesheetEntries']} timesheet entries, but got {report['numberOfTimesheetEntries']}"
    assert report["numberOfDatabaseEntries"] == expected_report["numberOfDatabaseEntries"], \
        f"Failed: Expected {expected_report['numberOfDatabaseEntries']} invalid entries, but got {report['numberOfDatabaseEntries']}"
    
    assert report["invalidEntries"] == expected_report["invalidEntries"], \
        f"Failed: Expected invalid entries {expected_report['invalidEntries']}, but got {report['invalidEntries']}"

    assert report["databaseHours"] == expected_report["databaseHours"], \
        f"Failed: Expected database hours {expected_report['databaseHours']}, but got {report['databaseHours']}"
    assert report["timesheetHours"] == expected_report["timesheetHours"], \
        f"Failed: Expected timesheet hours {expected_report['timesheetHours']}, but got {report['timesheetHours']}"
    
    print("Success: generate_report works as expected.")

def test_generate_report_single_entry_invalid_all_but_one(session):
    employee = Employee(name="Test User", email="test.email@example.com")
    session.add(employee)
    session.commit()

    event1 = Event(
        date="2023-12-03",
        hours=1,
        position="Teacher - Lead",
        location="Good Shepherd",
        employee_id=employee.id,
        name="Teaching Session"
    )                
        
    session.add(event1)
    session.commit()

    entry = [{"date": "2023-12-03", "hours": 1, "position": "Teacher - Lead", "location": "Good Shepherd"},
             {"date": "2023-12-11", "hours": 0, "position": "Teacher - Lead", "location": "False"},
             {"date": "2023-12-12", "hours": 0, "position": "Teacher - Lead", "location": "False"},
             {"date": "2023-12-13", "hours": 0, "position": "Teacher - Lead", "location": "False"}
    ]                         
    
    report = generate_report(employee.id, entry, session)
    
    expected_report = {
        "numberOfTimesheetEntries": 4,
        "numberOfDatabaseEntries": 1, 
        "invalidEntries": [                        
            {"date" : "2023-12-11", "hours": False, "position": False, "location": True },
            {"date" : "2023-12-12", "hours": False, "position": False, "location": True },
            {"date" : "2023-12-13", "hours": False, "position": False, "location": True }            
        ],
        "databaseHours": {
            "Teacher - Lead": 1,
        },
        "timesheetHours": {                        
        }
    }
    
    assert report["numberOfTimesheetEntries"] == expected_report["numberOfTimesheetEntries"], \
        f"Failed: Expected {expected_report['numberOfTimesheetEntries']} timesheet entries, but got {report['numberOfTimesheetEntries']}"
    
    assert report["numberOfDatabaseEntries"] == expected_report["numberOfDatabaseEntries"], \
        f"Failed: Expected {expected_report['numberOfDatabaseEntries']} invalid entries, but got {report['numberOfDatabaseEntries']}"
    
    assert report["invalidEntries"] == expected_report["invalidEntries"], \
        f"Failed: Expected invalid entries {expected_report['invalidEntries']}, but got {report['invalidEntries']}"

    assert report["databaseHours"] == expected_report["databaseHours"], \
        f"Failed: Expected database hours {expected_report['databaseHours']}, but got {report['databaseHours']}"
    
    print("Success: generate_report works as expected.")




# def test_single_event(session):
#     # Setup: Add a test employee and a single event to the database
#     employee = Employee(name="Test User", email="test.email@example.com")
#     session.add(employee)
#     session.commit()

#     # Add a corresponding event in the database
#     event = Event(
#     date=datetime.strptime('12/18/2023', '%m/%d/%Y'),  # or use '%Y-%m-%d' for '2023-12-18'
#         duration= 2.25,
#         position="Teacher - Lead",
#         location="Good Shepherd",
#         employee_id=employee.id,
#         name="Teaching Session"
#     )
#     session.add(event)
#     session.commit()

#     # Test: Generate a report with one timesheet entry
#     timesheet_entries = [
#         {"date": "12/18/2023", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"}
#     ]
    
#     report = generate_report(employee.id, timesheet_entries, session)
    
#     # Expected report structure
#     expected_report = {
#         "numberOfTimesheetEntries": 1,
#         "numberOfDatabaseEntries": 1,
#         "invalidEntries": {},
#         "databaseHours": {
#             "Teacher - Lead": 2.25
#         },
#         "timesheetHours": {
#             "Teacher - Lead": 2.25
#         }
#     }

#     assert report["numberOfTimesheetEntries"] == expected_report["numberOfTimesheetEntries"], \
#         f"Failed: Expected {expected_report['numberOfTimesheetEntries']} timesheet entries, but got {report['numberOfTimesheetEntries']}"
#     assert report["numberOfDatabaseEntries"] == expected_report["numberOfDatabaseEntries"], \
#         f"Failed: Expected {expected_report['numberOfDatabaseEntries']} invalid entries, but got {report['numberOfDatabaseEntries']}"
    
#     # Assertions for invalidEntries
#     assert report["invalidEntries"] == expected_report["invalidEntries"], \
#         f"Failed: Expected invalid entries {expected_report['invalidEntries']}, but got {report['invalidEntries']}"

#     # Assertions for databaseHours and timesheetHours
#     assert report["databaseHours"] == expected_report["databaseHours"], \
#         f"Failed: Expected database hours {expected_report['databaseHours']}, but got {report['databaseHours']}"
#     assert report["timesheetHours"] == expected_report["timesheetHours"], \
#         f"Failed: Expected timesheet hours {expected_report['timesheetHours']}, but got {report['timesheetHours']}"

#     print("Success: generate_report works as expected.")


# def test_multiple_events_exact_match_same_role(session):
#     # Setup: Add a test employee and multiple events for the same role on the same day
#     employee = Employee(name="Test User", email="test.email@example.com")
#     session.add(employee)
#     session.commit()

#     # Add multiple events on the same day with the same role
#     events = [
#         Event(
#             date=datetime.strptime('12/18/2023', '%m/%d/%Y'),  # or use '%Y-%m-%d' for '2023-12-18'
#             duration=2.25,
#             position="Teacher - Lead",
#             location="Good Shepherd",
#             employee_id=employee.id,
#             name="Morning Session"
#         ),
#         Event(
#             date=datetime.strptime('12/18/2023', '%m/%d/%Y'),  # or use '%Y-%m-%d' for '2023-12-18'
#             duration=2.00,
#             position="Teacher - Lead",
#             location="Good Shepherd",
#             employee_id=employee.id,
#             name="Afternoon Session"
#         )
#     ]
#     session.add_all(events)
#     session.commit()

#     # Test: Generate a report with two timesheet entries matching exactly with the database events
#     timesheet_entries = [
#         {"date": "12/18/2023", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"},
#         {"date": "12/18/2023", "hours": 2.00, "position": "Teacher - Lead", "location": "Good Shepherd"}
#     ]
    
#     report = generate_report(employee.id, timesheet_entries, session)
    
#     # Expected report structure
#     expected_report = {
#         "numberOfTimesheetEntries": 2,
#         "numberOfDatabaseEntries": 2,
#         "invalidEntries": {},
#         "databaseHours": {
#             "Teacher - Lead": 4.25
#         },
#         "timesheetHours": {
#             "Teacher - Lead": 4.25
#         }
#     }

#     assert report["numberOfTimesheetEntries"] == expected_report["numberOfTimesheetEntries"], \
#         f"Failed: Expected {expected_report['numberOfTimesheetEntries']} timesheet entries, but got {report['numberOfTimesheetEntries']}"
#     assert report["numberOfDatabaseEntries"] == expected_report["numberOfDatabaseEntries"], \
#         f"Failed: Expected {expected_report['numberOfDatabaseEntries']} database entries, but got {report['numberOfDatabaseEntries']}"
    
#     # Assertions for invalidEntries
#     assert report["invalidEntries"] == expected_report["invalidEntries"], \
#         f"Failed: Expected invalid entries {expected_report['invalidEntries']}, but got {report['invalidEntries']}"

#     # Assertions for databaseHours and timesheetHours
#     assert report["databaseHours"] == expected_report["databaseHours"], \
#         f"Failed: Expected database hours {expected_report['databaseHours']}, but got {report['databaseHours']}"
#     assert report["timesheetHours"] == expected_report["timesheetHours"], \
#         f"Failed: Expected timesheet hours {expected_report['timesheetHours']}, but got {report['timesheetHours']}"

#     print("Success: generate_report with exact match for multiple events on the same day works as expected.")


# def test_multiple_events_different_roles_same_day_ignore_time(session):
#     # Setup: Add a test employee and multiple events for different roles on the same day
#     employee = Employee(name="Test User", email="test.email@example.com")
#     session.add(employee)
#     session.commit()

#     # Add multiple events on the same day with different roles (time ignored)
#     events = [
#         Event(
#             date=datetime.strptime('12/18/2023', '%m/%d/%Y'),  # or use '%Y-%m-%d' for '2023-12-18'
#             duration=2.25,
#             position="Teacher - Lead",
#             location="Good Shepherd",
#             employee_id=employee.id,
#             name="Morning Session"
#         ),
#         Event(
#             date=datetime.strptime('12/18/2023', '%m/%d/%Y'),  # or use '%Y-%m-%d' for '2023-12-18'
#             duration=2.75,
#             position="Teacher - Assistant",
#             location="Good Shepherd",
#             employee_id=employee.id,
#             name="Afternoon Session"
#         )
#     ]
#     session.add_all(events)
#     session.commit()

#     # Test: Generate a report with two timesheet entries matching exactly with the database events (ignoring time)
#     timesheet_entries = [
#         {"date": "12/18/2023", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"},
#         {"date": "12/18/2023", "hours": 2.75, "position": "Teacher - Assistant", "location": "Good Shepherd"}
#     ]
    
#     report = generate_report(employee.id, timesheet_entries, session)
    
#     # Expected report structure
#     expected_report = {
#         "numberOfTimesheetEntries": 2,
#         "numberOfDatabaseEntries": 2,
#         "invalidEntries": {},
#         "databaseHours": {
#             "Teacher - Lead": 2.25,
#             "Teacher - Assistant": 2.75
#         },
#         "timesheetHours": {
#             "Teacher - Lead": 2.25,
#             "Teacher - Assistant": 2.75
#         }
#     }

#     assert report["numberOfTimesheetEntries"] == expected_report["numberOfTimesheetEntries"], \
#         f"Failed: Expected {expected_report['numberOfTimesheetEntries']} timesheet entries, but got {report['numberOfTimesheetEntries']}"
#     assert report["numberOfDatabaseEntries"] == expected_report["numberOfDatabaseEntries"], \
#         f"Failed: Expected {expected_report['numberOfDatabaseEntries']} invalid entries, but got {report['numberOfDatabaseEntries']}"
    
#     # Assertions for invalidEntries
#     assert report["invalidEntries"] == expected_report["invalidEntries"], \
#         f"Failed: Expected invalid entries {expected_report['invalidEntries']}, but got {report['invalidEntries']}"

#     # Assertions for databaseHours and timesheetHours
#     assert report["databaseHours"] == expected_report["databaseHours"], \
#         f"Failed: Expected database hours {expected_report['databaseHours']}, but got {report['databaseHours']}"
#     assert report["timesheetHours"] == expected_report["timesheetHours"], \
#         f"Failed: Expected timesheet hours {expected_report['timesheetHours']}, but got {report['timesheetHours']}"

#     print("Success: generate_report with exact match for different roles on the same day (ignoring time) works as expected.")


# def test_mismatched_events_and_timesheet_entries_ignore_time(session):
#     # Setup: Add a test employee and multiple events for different roles on the same day
#     employee = Employee(name="Test User", email="test.email@example.com")
#     session.add(employee)
#     session.commit()

#     # Add multiple events on the same day with different roles (time ignored)
#     events = [
#         Event(
#             date=datetime.strptime('12/18/2023', '%m/%d/%Y'),  # or use '%Y-%m-%d' for '2023-12-18'
#             duration=2.25,
#             position="Teacher - Lead",
#             location="Good Shepherd",
#             employee_id=employee.id,
#             name="Morning Session"
#         ),
#         Event(
#             date=datetime.strptime('12/18/2023', '%m/%d/%Y'),  # or use '%Y-%m-%d' for '2023-12-18'
#             duration=2.75,
#             position="Teacher - Assistant",
#             location="Good Shepherd",
#             employee_id=employee.id,
#             name="Afternoon Session"
#         )
#     ]
#     session.add_all(events)
#     session.commit()

#     # Test: Generate a report with timesheet entries that do not match exactly with the database events (ignoring time)
#     timesheet_entries = [
#         {"date": "12/18/2023", "hours": 2.25, "position": "Teacher - Lead", "location": "Good Shepherd"},
#         {"date": "12/18/2023", "hours": 3.00, "position": "Teacher - Assistant", "location": "Good Shepherd"}  # Mismatch in hours
#     ]
    
#     report = generate_report(employee.id, timesheet_entries, session)
    
#     # Expected report structure
#     expected_report = {
#         "numberOfTimesheetEntries": 2,
#         "numberOfInvalidEntries": 1,
#         "invalidEntries": {
#             "12/18/2023": {"date": True, "duration": False, "position": True, "location": True}  # Mismatch in duration
#         },
#         "databaseHours": {
#             "Teacher - Lead": 2.25,
#             "Teacher - Assistant": 2.75
#         },
#         "timesheetHours": {
#             "Teacher - Lead": 2.25,
#             "Teacher - Assistant": 3.00
#         }
#     }

#     assert report["numberOfTimesheetEntries"] == expected_report["numberOfTimesheetEntries"], \
#         f"Failed: Expected {expected_report['numberOfTimesheetEntries']} timesheet entries, but got {report['numberOfTimesheetEntries']}"
#     assert report["numberOfInvalidEntries"] == expected_report["numberOfInvalidEntries"], \
#         f"Failed: Expected {expected_report['numberOfInvalidEntries']} invalid entries, but got {report['numberOfInvalidEntries']}"
    
#     # Assertions for invalidEntries
#     assert report["invalidEntries"] == expected_report["invalidEntries"], \
#         f"Failed: Expected invalid entries {expected_report['invalidEntries']}, but got {report['invalidEntries']}"

#     # Assertions for databaseHours and timesheetHours
#     assert report["databaseHours"] == expected_report["databaseHours"], \
#         f"Failed: Expected database hours {expected_report['databaseHours']}, but got {report['databaseHours']}"
#     assert report["timesheetHours"] == expected_report["timesheetHours"], \
#         f"Failed: Expected timesheet hours {expected_report['timesheetHours']}, but got {report['timesheetHours']}"

#     print("Success: generate_report with mismatched entries on the same day (ignoring time) works as expected.")
