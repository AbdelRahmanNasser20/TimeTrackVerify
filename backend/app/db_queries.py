from .models import Employee, Event
from .extensions import db

def count_entries_for_employee(employee_id, session=db.session):
    """
    Counts the number of entries in the database for a given employee.
    """
    try:
        count = session.query(Event).filter_by(employee_id=employee_id).count()        
        print(f"Found {count} entries for employee ID {employee_id}")
        return count
    except Exception as e:
        print(f"Error counting entries for employee ID {employee_id}: {e}")
        return 0

def retrieve_all_db_events_for_employee(employee_id, session=db.session):    
    try:
        events = session.query(Event).filter_by(employee_id=employee_id).all()
        return events
    except Exception as e:
        print(f"Error retrieving all entries for employee ID {employee_id}: {e}")
        return []


def get_employee_id(email,session=db.session):
    """
    Retrieves the employee ID using the provided email.
    """
    try:
        employee = session.query(Employee).filter_by(email=email).first()
        if not employee:            
            print(f"No employee found for email {email}")
            return None
        
        return employee.id        
        
    except Exception as e:
        print(f"Error retrieving employee ID for email {email}: {e}")
        return None

def get_events_for_employee_by_date(employee_id, date,session = db.session):
    """
    Fetches all events from the database for a given employee on a specific date.

    :param employee_id: ID of the employee
    :param date: The date of the event
    :return: A list of database rows for the events, or an empty list if no events are found
    """
    try:
        events = session.query(Event).filter_by(employee_id=employee_id, date=date).all()
        if not events:
            print(f"No events found for employee ID {employee_id} on date {date}")
           
        # print(f"Found {len(events)} events for employee ID {employee_id} on date {date}")
        return events        
    
    except Exception as e:
        print(f"Error retrieving events for employee ID {employee_id} on date {date}: {e}")
        return []
    


def sum_hours_by_role_from_db(employee_id,session=db.session):
    """
    Fetches all entries for a given employee from the database and sums up the hours for each role.
    """
    total_hours_by_role = {}
    
    events = retrieve_all_db_events_for_employee(employee_id, session)
    
    for event in events:        
        role = event.position
        hours = float(event.duration)  # Ensure hours is a float

        if role in total_hours_by_role:
            total_hours_by_role[role] += hours
        else:
            total_hours_by_role[role] = hours        
    
    return total_hours_by_role


from datetime import datetime

def get_events_for_month(employee_id: int, month_year: str, session=db.session):
    """
    Retrieves all events for a specific employee within a given month.

    :param employee_id: The ID of the employee.
    :param month_year: The month and year in 'MM/YYYY' format (e.g., '12/2023').
    :return: A list of dictionaries, each representing an event.
    """
    try:
        # check to ensure it can cover the end of the month
        # Reformat the month_year input to match the database format
        start_date = datetime.strptime(month_year, '%m/%Y').strftime('%Y-%m-01')
        end_date = datetime.strptime(month_year, '%m/%Y').strftime('%Y-%m-31')

        # Query the database for events within the specified month
        events = session.query(Event).filter(
            Event.employee_id == employee_id,
            Event.date >= start_date,
            Event.date <= end_date
        ).all()

        # Format the results
        formatted_events = [
            {
                "date": event.date.strftime('%m/%d/%Y'),
                "hours": float(event.duration),
                "position": event.position,
                "location": event.location
            }
            for event in events
        ]
        
        return formatted_events

    except Exception as e:
        print(f"Error retrieving events for employee ID {employee_id} in month {month_year}: {e}")
        return []
