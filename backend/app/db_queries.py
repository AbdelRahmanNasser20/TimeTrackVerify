from calendar import monthrange

from pytest import Session
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

def retrieve_all_db_events_for_employee(employee_id, session=db.session):    
    try:
        events = session.query(Event).filter_by(employee_id=employee_id).all()
        return events
    except Exception as e:
        print(f"Error retrieving all entries for employee ID {employee_id}: {e}")
        return []
    
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
        hours = event.hours

        if role in total_hours_by_role:
            total_hours_by_role[role] += hours
        else:
            total_hours_by_role[role] = hours        
    
    return total_hours_by_role


from datetime import datetime

def get_events_for_month(employee_id: int, date_input: str or datetime.date, session: Session = db.session):
    """
    Retrieves all events for a specific employee within the month of the given date.

    :param employee_id: The ID of the employee.
    :param date_str: A date in 'MM/DD/YYYY' format (e.g., '12/03/2023').
    :param session: SQLAlchemy session object.
    :return: A list of dictionaries, each representing an event.
    """
    try:

        print('date_input',date_input)
         # Determine if the input is a string or a datetime.date object
        if isinstance(date_input, str):
            # Try to parse as 'YYYY-MM-DD' first
            try:
                input_date = datetime.strptime(date_input, '%Y-%m-%d').date()
            except ValueError:
                # If that fails, try to parse as 'MM/DD/YYYY'
                input_date = datetime.strptime(date_input, '%m/%d/%Y').date()
        elif isinstance(date_input, datetime.date):
            input_date = date_input
        else:
            raise ValueError("Invalid date format. Please use 'YYYY-MM-DD' or 'MM/DD/YYYY' or a date object.")
        
        print('input_date',input_date)
        first_day_of_month = input_date.replace(day=1)
        last_day_of_month = input_date.replace(day=monthrange(input_date.year, input_date.month)[1])


        # Query the database for events within the specified date range
        events = session.query(Event).filter(
            Event.employee_id == employee_id,
            Event.date >= first_day_of_month,
            Event.date <= last_day_of_month
        ).all()
        

        # Format the results
        formatted_events = [
            {
                "date": event.date.strftime('%Y-%m-%d'),
                "hours": event.hours,
                "position": event.position,
                "location": event.location
            }
            for event in events
        ]
        
        return formatted_events

    except ValueError as e:
        print(f"An error occurred: {e}")
        raise
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
        


def get_event_by_date_position(employee_id, date, position, hours = 0, session=db.session):
    """
    Retrieves a specific event from the database based on date, position, and duration.

    :param employee_id: The ID of the employee.
    :param date: The date of the event.
    :param position: The position of the event.
    :param hours: The hours of the event.
    :return: The matching Event object or None if not found.
    """
    try:
        event = session.query(Event).filter_by(
            employee_id=employee_id,
            date=date,
            position=position,
        ).first()

        if event:
            # Format the date in MM/DD/YYYY format
            event.date = event.date.strftime('%Y-%m-%d')
        return event
    except ValueError as e:
        print(f"An error occurred: {e}")
        raise  # Re-raise the exception to ensure the test catches it
    except TypeError as e:
        print(f"An error occurred: {e}")
        raise  # Re-raise the exception to ensure the test catches it

    

def get_events_by_date(employee_id, date, session=db.session):
    """
    Retrieves all events for a specific employee on a given date.

    :param employee_id: The ID of the employee.
    :param date: The date of the events.
    :return: A list of Event objects.
    """
    try:
        events = session.query(Event).filter_by(
            employee_id=employee_id,
            date=date
        ).all()
        
        # Format the dates in MM/DD/YYYY format
        formatted_events = []
        for event in events:
            formatted_event = {
                "date": event.date.strftime('%Y-%m-%d'),
                "hours": event.hours,
                "position": event.position,
                "location": event.location
            }
            formatted_events.append(formatted_event)

        if not events:
            print(f"No events found for employee ID {employee_id} on date {date}")

        return formatted_events
    except Exception as e:
        print(f"Error retrieving events for date {date}: {e}")
        return []