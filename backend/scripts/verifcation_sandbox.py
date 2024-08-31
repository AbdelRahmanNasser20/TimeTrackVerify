import os , sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import Employee, Event
from app.extensions import db
from app.db_queries import get_employee_id, get_events_by_date, get_events_for_employee_by_date, get_events_for_month
from app.new_validate_timesheet import validate_timesheet_entry_against_db, reformat_date, sum_hours_by_role, generate_report


# Create your Flask app
app = create_app()

# Activate the application context
with app.app_context():

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
    [{'date': '2023-12-03', 'hours': 2.25, 'location': 'Good Shepherd ', 'position': 'Teacher - Lead'}, {'date': '2023-12-03', 'hours': 2, 'location': 'Oakland Terrace ES', 'position': 'Teacher - Assistant'}, {'date': '2023-12-05', 'hours': 2.75, 'location': 'Burning Tree ES', 'position': 'Teacher - Assistant'}, {'date': '2023-12-06', 'hours': 2.5, 'location': 'Forest knolls ES', 'position': 'Teacher - Lead'}, {'date': '2023-12-11', 'hours': 2.5, 'location': 'ST andrew', 'position': 'Teacher - Lead'}, {'date': '2023-12-13', 'hours': 2.5, 'location': 'Forest knolls ES', 'position': 'Teacher - Lead'}, {'date': '2023-12-18', 'hours': 2.5, 'location': 'ST andrew', 'position': 'Teacher - Lead'}, {'date': '2023-12-20', 'hours': 2.5, 'location': 'Forest knolls ES', 'position': 'Teacher - Lead'}]

    print("THIS IS THE ENTRY", reformat_date(timesheet_entries[0]['date']))
    abdels_id = get_employee_id("abdel.nasser045@gmail.com")
    
    print("abdels_id", abdels_id)
    db_entries = get_events_for_month(abdels_id, "2023-12-03")   
    print(db_entries[0]["date"],db_entries[0]["position"]) 
    
    # print(sum_hours_by_role(timesheet_entries))
    # print(sum_hours_by_role(db_entries))
    
    report = generate_report(abdels_id, timesheet_entries)
    print(report)
    # ts_entry = timesheet_entries[0]
    # print("Entry on " , reformat_date(ts_entry["date"]) , " " , get_events_by_date(abdels_id, ts_entry["date"]))
        
    # validation = validate_timesheet_entry_against_db(abdels_id, ts_entry)
    
    # validations = {}
    # for entry in timesheet_entries:
    #     validation = validate_timesheet_entry_against_db(abdels_id, entry)
    #     print(validation)
    #     validations[entry["date"]] = validation

    # print(validations)
    # print("Invalid entries: ", find_invalid_entries(validations))
    