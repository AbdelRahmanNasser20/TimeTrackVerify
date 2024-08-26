import pytest
from app.models import Employee, Event
from app.db_queries import (
    count_entries_for_employee,
    get_employee_id,
    get_events_for_employee_by_date,
    retrieve_all_db_events_for_employee
)

def test_add_employee(session):
    
    new_employee = Employee(name='Jane Smith', email='jane.smith@example.com')
    session.add(new_employee)
    session.commit()

    employee = session.query(Employee).filter_by(email='jane.smith@example.com').first()
    assert employee is not None, "Failed to add the new employee"
    assert employee.name == 'Jane Smith', f"Employee name mismatch, expected 'Jane Smith' but got {employee.name}"

def test_remove_employee(session):
    employee = Employee(name='John Doe', email='john.doe@example.com')
    session.add(employee)
    session.commit()

    session.delete(employee)
    session.commit()

    employee = session.query(Employee).filter_by(email='john.doe@example.com').first()
    assert employee is None, "Failed to remove the employee"

def test_add_event(session):
    employee = Employee(name='John Doe', email='john.doe@example.com')
    session.add(employee)
    session.commit()

    new_event = Event(
        name='Conference', date='2024-07-01', duration='3.0',
        position='Speaker', location='Auditorium', employee_id=employee.id
    )
    session.add(new_event)
    session.commit()

    event = session.query(Event).filter_by(name='Conference').first()
    assert event is not None, "Failed to add the new event"
    assert event.position == 'Speaker', f"Event position mismatch, expected 'Speaker' but got {event.position}"

def test_count_entries_for_employee(session):
    employee = Employee(name='John Doe', email='john.doe@example.com')
    session.add(employee)
    session.commit()

    event1 = Event(
        name='Meeting', date='2024-06-20', duration='1.0',
        position='Manager', location='Office', employee_id=employee.id
    )
    event2 = Event(
        name='Workshop', date='2024-06-21', duration='2.5',
        position='Teacher', location='Conference Room', employee_id=employee.id
    )
    session.add(event1)
    session.add(event2)
    session.commit()

    count = count_entries_for_employee(employee.id, session)
    assert count == 2, f"Expected 2 entries but got {count}"

def test_retrieve_all_db_events_for_employee(session):

    employee = Employee(name='John Doe', email='john.doe@example.com')
    session.add(employee)
    session.commit()

    event1 = Event(
        name='Meeting', date='2024-06-20', duration='1.0',
        position='Manager', location='Office', employee_id=employee.id
    )
    event2 = Event(
        name='Workshop', date='2024-06-21', duration='2.5',
        position='Teacher', location='Conference Room', employee_id=employee.id
    )
    session.add(event1)
    session.add(event2)
    session.commit()

    retrieve_all_db_events_for_employee(employee.id, session)
    

def test_get_employee_id(session):
    employee = Employee(name='John Doe', email='john.doe@example.com')
    session.add(employee)
    session.commit()

    employee_id = get_employee_id('john.doe@example.com', session)
    assert employee_id is not None, "Failed to retrieve the employee ID"
    assert employee_id == employee.id, f"Expected employee ID {employee.id} but got {employee_id}"

def test_get_events_for_employee_by_date(session):
    employee = Employee(name='John Doe', email='john.doe@example.com')
    session.add(employee)
    session.commit()

    event = Event(
        name='Meeting', date='2024-06-20', duration='1.0',
        position='Manager', location='Office', employee_id=employee.id
    )
    session.add(event)
    session.commit()

    events = get_events_for_employee_by_date(employee.id, '2024-06-20', session)
    assert len(events) == 1, f"Expected 1 event but got {len(events)}"
    assert events[0].name == 'Meeting', f"Expected event name 'Meeting' but got {events[0].name}"
    assert events[0].position == 'Manager', f"Expected position 'Manager' but got {events[0].position}"

def test_remove_event(session):
    employee = Employee(name='John Doe', email='john.doe@example.com')
    session.add(employee)
    session.commit()

    event = Event(
        name='Meeting', date='2024-06-20', duration='1.0',
        position='Manager', location='Office', employee_id=employee.id
    )
    session.add(event)
    session.commit()

    session.delete(event)
    session.commit()

    removed_event = session.query(Event).filter_by(name='Meeting').first()
    assert removed_event is None, "Failed to remove the event"



