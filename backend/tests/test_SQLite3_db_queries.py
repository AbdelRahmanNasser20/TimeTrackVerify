# import pytest
# from app.models import Employee, Event
# from datetime import datetime
# @pytest.mark.db_tests
# @pytest.fixture(autouse=True)
# def clean_up_session(db):
#     """Ensure the database session is rolled back between tests."""
#     db.session.rollback()
# @pytest.mark.db_tests
# def test_add_employee(db):
#     """Test adding an employee to the database."""
#     new_employee = Employee(name='Jane Doe', email='jane.doe.unique@example.com')
#     db.session.add(new_employee)
#     db.session.commit()

#     # Verify the new employee was added
#     employee = Employee.query.filter_by(email='jane.doe.unique@example.com').first()
#     assert employee is not None, "Failed to add the new employee"
#     assert employee.name == 'Jane Doe'
# @pytest.mark.db_tests
# def test_remove_employee(db):
#     """Test removing an employee from the database."""
#     employee = Employee(name='John Smith', email='john.smith.unique@example.com')
#     db.session.add(employee)
#     db.session.commit()

#     db.session.delete(employee)
#     db.session.commit()

#     # Verify the employee was removed
#     employee = Employee.query.filter_by(email='john.smith.unique@example.com').first()
#     assert employee is None, "Failed to remove the employee"
# @pytest.mark.db_tests
# def test_add_event(db):
#     """Test adding an event to the database."""
#     employee = Employee(name='John Smith', email='john.smith.event@example.com')
#     db.session.add(employee)
#     db.session.commit()

#     event_date = datetime.strptime('2024-07-01', '%Y-%m-%d')
#     new_event = Event(
#         name='Conference', date=event_date, duration='3.0',
#         position='Speaker', location='Auditorium', employee_id=employee.id
#     )
#     db.session.add(new_event)
#     db.session.commit()

#     # Verify the new event was added
#     event = Event.query.filter_by(name='Conference').first()
#     assert event is not None, "Failed to add the new event"
#     assert event.position == 'Speaker'
# @pytest.mark.db_tests
# def test_remove_event(db):
#     """Test removing an event from the database."""
#     employee = Employee(name='John Smith', email='john.smith.removeevent@example.com')
#     db.session.add(employee)
#     db.session.commit()

#     event_date = datetime.strptime('2024-07-01', '%Y-%m-%d')
#     new_event = Event(
#         name='Conference', date=event_date, duration='3.0',
#         position='Speaker', location='Auditorium', employee_id=employee.id
#     )
#     db.session.add(new_event)
#     db.session.commit()

#     db.session.delete(new_event)
#     db.session.commit()

#     # Verify the event was removed
#     event = Event.query.filter_by(name='Conference').first()
#     assert event is None, "Failed to remove the event"
# @pytest.mark.db_tests
# def test_count_entries_for_employee(db):
#     """Test counting the number of entries for an employee."""
#     employee = Employee(name='Alice Doe', email='alice.doe.count@example.com')
#     db.session.add(employee)
#     db.session.commit()

#     event_date1 = datetime.strptime('2024-06-20', '%Y-%m-%d')
#     event_date2 = datetime.strptime('2024-06-21', '%Y-%m-%d')

#     new_event1 = Event(
#         name='Meeting', date=event_date1, duration='1.0',
#         position='Manager', location='Office', employee_id=employee.id
#     )
#     new_event2 = Event(
#         name='Workshop', date=event_date2, duration='2.5',
#         position='Teacher', location='Conference Room', employee_id=employee.id
#     )
#     db.session.add(new_event1)
#     db.session.add(new_event2)
#     db.session.commit()

#     # Count the number of events
#     count = Event.query.filter_by(employee_id=employee.id).count()
#     assert count == 2, f"Expected 2 events, but got {count}"
# @pytest.mark.db_tests
# def test_sum_hours_by_role_from_db(db):
#     """Test summing hours by role for an employee."""
#     employee = Employee(name='Alice Doe', email='alice.doe.sum@example.com')
#     db.session.add(employee)
#     db.session.commit()

#     event_date1 = datetime.strptime('2024-06-20', '%Y-%m-%d')
#     event_date2 = datetime.strptime('2024-06-21', '%Y-%m-%d')

#     new_event1 = Event(
#         name='Meeting', date=event_date1, duration='1.0',
#         position='Manager', location='Office', employee_id=employee.id
#     )
#     new_event2 = Event(
#         name='Workshop', date=event_date2, duration='2.5',
#         position='Teacher', location='Conference Room', employee_id=employee.id
#     )
#     db.session.add(new_event1)
#     db.session.add(new_event2)
#     db.session.commit()

#     # Sum hours by role
#     manager_hours = db.session.query(db.func.sum(Event.duration)).filter_by(employee_id=employee.id, position='Manager').scalar()
#     teacher_hours = db.session.query(db.func.sum(Event.duration)).filter_by(employee_id=employee.id, position='Teacher').scalar()

#     assert manager_hours == 1.0, f"Expected 1.0 hours for Manager, but got {manager_hours}"
#     assert teacher_hours == 2.5, f"Expected 2.5 hours for Teacher, but got {teacher_hours}"
# @pytest.mark.db_tests
# def test_get_employee_id(db):
#     """Test getting an employee ID by email."""
#     employee = Employee(name='Alice Doe', email='alice.doe.getid@example.com')
#     db.session.add(employee)
#     db.session.commit()

#     retrieved_employee = Employee.query.filter_by(email='alice.doe.getid@example.com').first()
#     assert retrieved_employee is not None, "Failed to retrieve employee"
#     assert retrieved_employee.id == employee.id, f"Expected employee ID {employee.id}, but got {retrieved_employee.id}"
# @pytest.mark.db_tests
# def test_remove_event(db):
#     """Test removing an event from the database."""
#     # Create and add a new employee
#     employee = Employee(name='John Smith', email='john.smith.removeevent@example.com')
#     db.session.add(employee)
#     db.session.commit()

#     # Create and add a new event
#     event_date = datetime.strptime('2024-07-01', '%Y-%m-%d')
#     new_event = Event(
#         name='Conference', date=event_date, duration='3.0',
#         position='Speaker', location='Auditorium', employee_id=employee.id
#     )
#     db.session.add(new_event)
#     db.session.commit()

#     # Verify the event was added
#     added_event = Event.query.filter_by(name='Conference').first()
#     assert added_event is not None, "Failed to add the event"

#     # Remove the event
#     db.session.delete(added_event)
#     db.session.commit()

#     # Flush the session and check again
#     db.session.flush()

#     # Verify the event was removed
#     event = Event.query.filter_by(name='Conference').first()
#     print(f"Event after deletion attempt: {event}")  # Debug information
#     assert event is None, "Failed to remove the event"