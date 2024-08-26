import pytest
from app.verify_timesheet import sum_hours_by_role_from_db, generate_report, process_timesheet_entries
from app.models import Employee, Event
from app.db_queries import get_events_for_month


from datetime import datetime

def test_get_events_for_month(session):
    # Create a dummy employee
    employee = Employee(name='John Doe', email='john.doe@example.com')
    session.add(employee)
    session.commit()

    # Add events to the database
    event1 = Event(
        name = 'Event 1',
        date=datetime.strptime('2023-12-01', '%Y-%m-%d'),
        duration=5.0,
        position='Teacher - Lead',
        location='School A',
        employee_id=employee.id
    )
    event2 = Event(
        name = 'Event 2',
        date=datetime.strptime('2023-12-03', '%Y-%m-%d'),
        duration=3.0,
        position='Teacher - Assistant',
        location='School B',
        employee_id=employee.id
    )
    event3 = Event(
        name = 'Event 1',
        date=datetime.strptime('2023-11-25', '%Y-%m-%d'),
        duration=4.0,
        position='Teacher - Lead',
        location='School C',
        employee_id=employee.id
    )
    session.add(event1)
    session.add(event2)
    session.add(event3)
    session.commit()

    # Test the function for December 2023
    result = get_events_for_month(employee.id, '12/2023', session)

    # Expected result
    expected_result = [
        {"date": '12/01/2023', "hours": 5.0, "position": 'Teacher - Lead', "location": 'School A'},
        {"date": '12/03/2023', "hours": 3.0, "position": 'Teacher - Assistant', "location": 'School B'}
    ]        
    
    assert result == expected_result, f"Expected {expected_result} but got {result}"

    # Test for an empty month
    result_empty = get_events_for_month(employee.id, '11/2023', session)

    assert len(result_empty) == 0, f"Expected no events but got {result_empty}"
    
def test_sum_hours_same_day_different_positions(session):
    employee = Employee(name='John Doe', email='john.doe@example.com')
    session.add(employee)
    session.commit()

    event_date = '2024-06-20'
    event1 = Event(
        name='Morning Meeting', date=event_date, duration='1.5',
        position='Manager', location='Office', employee_id=employee.id
    )
    event2 = Event(
        name='Afternoon Meeting', date=event_date, duration='2.0',
        position='Manager', location='Office', employee_id=employee.id
    )

    event3 = Event(
        name='Evening Workshop', date=event_date, duration='2.5',
        position='Teacher', location='Conference Room', employee_id=employee.id
    )

    session.add(event1)
    session.add(event2)
    session.add(event3)
    session.commit()

    hours_by_role = sum_hours_by_role_from_db(employee.id, session)

    assert hours_by_role['Manager'] == 3.5, f"Expected 3.5 hours for Manager but got {hours_by_role['Manager']}"
    assert hours_by_role['Teacher'] == 2.5, f"Expected 2.5 hours for Teacher but got {hours_by_role['Teacher']}"


# def test_MOCK_sum_hours_same_day_different_positions():
#     # Create mock timesheet entries
#     timesheet_entries = [
#         {"date": '12/01/2023', "hours": 5.0, "position": 'Teacher - Lead', "location": 'School A'},
#         {"date": '12/01/2023', "hours": 2.0, "position": 'Teacher - Assistant', "location": 'School A'},
#         {"date": '12/02/2023', "hours": 3.0, "position": 'Teacher - Assistant', "location": 'School B'},
#         {"date": '12/02/2023', "hours": 4.0, "position": 'Teacher - Lead', "location": 'School B'}
#     ]
    
#     # Create mock database entries
#     db_entries = [
#         {'date': '2023-12-01', 'position': 'Teacher - Lead', 'hours': '5.0', 'location': 'School A'},
#         {'date': '2023-12-01', 'position': 'Teacher - Assistant', 'hours': '2.0', 'location': 'School A'},
#         {'date': '2023-12-02', 'position': 'Teacher - Assistant', 'hours': '3.0', 'location': 'School B'},
#         {'date': '2023-12-02', 'position': 'Teacher - Lead', 'hours': '4.0', 'location': 'School B'}
#     ]
    
#     # Generate a report using the mock data
#     report = generate_report(db_entries, timesheet_entries)
    
#     print("Report:", report)
#     # Assert that the report is correct
#     assert report['numberOfTimesheetEntries'] == 4, f"Expected 4 timesheet entries but got {report['numberOfTimesheetEntries']}"
#     assert report['numberOfDatabaseEntries'] == 4, f"Expected 4 database entries but got {report['numberOfDatabaseEntries']}"
#     assert report['databaseHours']['Teacher - Lead'] == 9.0, f"Expected 9.0 hours for Teacher - Lead but got {report['databaseHours']['Teacher - Lead']}"
#     assert report['databaseHours']['Teacher - Assistant'] == 5.0, f"Expected 5.0 hours for Teacher - Assistant but got {report['databaseHours']['Teacher - Assistant']}"
#     assert report['timesheetHours']['Teacher - Lead'] == 9.0, f"Expected 9.0 hours for Teacher - Lead but got {report['timesheetHours']['Teacher - Lead']}"
#     assert report['timesheetHours']['Teacher - Assistant'] == 5.0, f"Expected 5.0 hours for Teacher - Assistant but got {report['timesheetHours']['Teacher - Assistant']}"
    
    # Process and verify invalid entries
    # invalid_entries = process_timesheet_entries(db_entries, timesheet_entries)  # You can mock this as well if needed
    # assert len(invalid_entries) == 0, f"Expected no invalid entries, but got {invalid_entries}"



# def test_sum_hours_same_day_different_positions(session):
#     # Create an employee and commit to the session
#     employee = Employee(name='John Doe', email='john.doe@example.com')
    
#     session.add(employee)
#     session.commit()
#     print("Employee ID:", employee.id)

#     # Insert events into the database for the employee
#     event_date1 = '2023-12-01'
#     event1 = Event(
#         name='Event 1',  # Provide a name for the event
#         date=event_date1, duration='5.0',
#         position='Teacher - Lead', location='School A', employee_id=employee.id
#     )
#     event2 = Event(
#         name='Event 2',  # Provide a name for the event
#         date=event_date1, duration='2.0',
#         position='Teacher - Assistant', location='School A', employee_id=employee.id
#     )
    
#     event_date2 = '2023-12-02'
#     event3 = Event(
#         name='Event 3',  # Provide a name for the event
#         date=event_date2, duration='3.0',
#         position='Teacher - Assistant', location='School B', employee_id=employee.id
#     )
#     event4 = Event(
#         name='Event 4',  # Provide a name for the event
#         date=event_date2, duration='4.0',
#         position='Teacher - Lead', location='School B', employee_id=employee.id
#     )

#     session.add(event1)
#     session.add(event2)
#     session.add(event3)
#     session.add(event4)
#     session.commit()

#     # Define timesheet entries that mirror the database events
#     timesheet_entries = [
#         {'date': '2023-12-01', 'position': 'Teacher - Lead', 'hours': '5.0', 'location': 'School A'},
#         {'date': '2023-12-01', 'position': 'Teacher - Assistant', 'hours': '2.0', 'location': 'School A'},
#         {'date': '2023-12-02', 'position': 'Teacher - Assistant', 'hours': '3.0', 'location': 'School B'},
#         {'date': '2023-12-02', 'position': 'Teacher - Lead', 'hours': '4.0', 'location': 'School B'}
#     ]
    
#     # Generate a report using the function
#     report = generate_report(employee.id, timesheet_entries)
    
#     print("Report:", report)
#     # Assert that the report is correct
#     assert report['numberOfTimesheetEntries'] == 4, f"Expected 4 timesheet entries but got {report['numberOfTimesheetEntries']}"
#     assert report['numberOfDatabaseEntries'] == 4, f"Expected 4 database entries but got {report['numberOfDatabaseEntries']}"
#     assert report['databaseHours']['Teacher - Lead'] == 9.0, f"Expected 9.0 hours for Teacher - Lead but got {report['databaseHours']['Teacher - Lead']}"
#     assert report['databaseHours']['Teacher - Assistant'] == 5.0, f"Expected 5.0 hours for Teacher - Assistant but got {report['databaseHours']['Teacher - Assistant']}"
#     assert report['timesheetHours']['Teacher - Lead'] == 9.0, f"Expected 9.0 hours for Teacher - Lead but got {report['timesheetHours']['Teacher - Lead']}"
#     assert report['timesheetHours']['Teacher - Assistant'] == 5.0, f"Expected 5.0 hours for Teacher - Assistant but got {report['timesheetHours']['Teacher - Assistant']}"

#     # Process and verify invalid entries
#     invalid_entries = process_timesheet_entries(employee.id, timesheet_entries)
#     assert len(invalid_entries) == 0, f"Expected no invalid entries, but got {invalid_entries}"



# import pytest
# from app.verify_timesheet import reformat_date, sum_hours_by_position_from_timesheet, validate_entry, process_timesheet_entries, generate_report
# from app.db_queries import get_events_for_employee_by_date, count_entries_for_employee, sum_hours_by_role_from_db
# from app.models import Event, Employee
# from unittest.mock import patch


# def test_reformat_date():
#     assert reformat_date('2023-12-01') == '12/01/2023'
#     assert reformat_date('2023-02-28') == '02/28/2023'
#     assert reformat_date('invalid-date') == 'Invalid date format'


# def test_sum_hours_by_position_from_timesheet():
#     timesheet_entries = [
#         {'position': 'Manager', 'hours': '1.5'},
#         {'position': 'Manager', 'hours': '2.0'},
#         {'position': 'Teacher', 'hours': '2.5'}
#     ]
#     result = sum_hours_by_position_from_timesheet(timesheet_entries)
#     assert result['Manager'] == 3.5, f"Expected 3.5 hours for Manager but got {result['Manager']}"
#     assert result['Teacher'] == 2.5, f"Expected 2.5 hours for Teacher but got {result['Teacher']}"


# @patch('app.verify_timesheet.get_events_for_employee_by_date')
# def test_validate_entry(mock_get_events):
#     mock_db_entry = Event('12/01/2023', 5.0, 'Teacher - Lead', 'School A')
#     timesheet_entry = {'date': '2023-12-01', 'position': 'Teacher - Lead', 'hours': '5.0', 'location': 'School A'}
    
#     result = validate_entry(mock_db_entry, timesheet_entry)
#     assert result['date'] == '12/01/2023'
#     assert result['duration'] is True
#     assert result['location'] is True
#     assert result['position'] is True


# @patch('app.verify_timesheet.get_events_for_employee_by_date')
# def test_process_timesheet_entries(mock_get_events):
#     mock_db_entry = Event('12/01/2023', 5.0, 'Teacher - Lead', 'School A')
#     mock_get_events.return_value = mock_db_entry

#     timesheet_entries = [
#         {'date': '2023-12-01', 'position': 'Teacher - Lead', 'hours': '5.0', 'location': 'School A'},
#         {'date': '2023-12-01', 'position': 'Teacher - Assistant', 'hours': '2.0', 'location': 'School A'},
#     ]
#     invalid_entries = process_timesheet_entries(1, timesheet_entries)
#     assert len(invalid_entries) == 1, f"Expected 1 invalid entry but got {len(invalid_entries)}"
#     assert invalid_entries[0]['position'] is False


# @patch('app.verify_timesheet.count_entries_for_employee')
# @patch('app.verify_timesheet.sum_hours_by_role_from_db')
# def test_generate_report(mock_sum_hours, mock_count_entries):
#     mock_sum_hours.return_value = {'Manager': 3.5, 'Teacher': 2.5}
#     mock_count_entries.return_value = 2
    
#     timesheet_entries = [
#         {'date': '2023-12-01', 'position': 'Teacher - Lead', 'hours': '5.0', 'location': 'School A'},
#         {'date': '2023-12-01', 'position': 'Teacher - Assistant', 'hours': '2.0', 'location': 'School A'},
#     ]
    
#     report = generate_report(1, timesheet_entries)
#     assert report['numberOfTimesheetEntries'] == 2
#     assert report['numberOfDatabaseEntries'] == 2
#     assert report['databaseHours'] == {'Manager': 3.5, 'Teacher': 2.5}
#     assert report['timesheetHours']['Teacher - Lead'] == 5.0
