from .models import Employee, Event
from .extensions import db

def count_entries_for_employee(employee_id):
    """
    Counts the number of entries in the database for a given employee.
    """
    try:
        count = db.session.query(Event).filter_by(employee_id=employee_id).count()
        print(f"Counted {count} entries for employee ID {employee_id}")
        return count
    except Exception as e:
        print(f"Error counting entries for employee ID {employee_id}: {e}")
        return 0

def sum_hours_by_role_from_db(employee_id):
    """
    Fetches all entries for a given employee from the database and sums up the hours for each role.
    """
    total_hours_by_role = {}
    try:
        events = db.session.query(Event).filter_by(employee_id=employee_id).all()
        for event in events:
            role = event.position
            hours = float(event.duration)  # Ensure hours is a float

            if role in total_hours_by_role:
                total_hours_by_role[role] += hours
            else:
                total_hours_by_role[role] = hours
        print(f"Summed hours by role for employee ID {employee_id}: {total_hours_by_role}")
    except Exception as e:
        print(f"Error summing hours by role for employee ID {employee_id}: {e}")

    return total_hours_by_role

def get_employee_id(email):
    """
    Retrieves the employee ID using the provided email.
    """
    try:
        employee = db.session.query(Employee).filter_by(email=email).first()
        if employee:
            print(f"Found employee ID {employee.id} for email {email}")
            return employee.id
        else:
            print(f"No employee found for email {email}")
            return None
    except Exception as e:
        print(f"Error retrieving employee ID for email {email}: {e}")
        return None

def get_events_for_employee_by_date(employee_id, date):
    """
    Fetches events from the database for a given employee on a specific date.

    :param employee_id: ID of the employee
    :param date: The date of the event
    :return: The database row for the event, or None if no event is found
    """
    try:
        event = db.session.query(Event).filter_by(employee_id=employee_id, date=date).first()
        if event:
            print(f"Found event for employee ID {employee_id} on date {date}")
        else:
            print(f"No event found for employee ID {employee_id} on date {date}")
        return event
    except Exception as e:
        print(f"Error retrieving event for employee ID {employee_id} on date {date}: {e}")
        return None
