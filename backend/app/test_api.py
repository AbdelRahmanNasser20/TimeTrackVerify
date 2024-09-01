import os
import requests
import pytest

# Ensure environment variables are set for testing
# os.environ['DATABASE_URL'] = 'postgresql://abdelnasser:greatness@db:5432/mydatabase'
# os.environ['FLASK_ENV'] = 'testing'

# BASE_URL = 'http://backend:5001'
BASE_URL = 'http://0.0.0.0:5001'

def test_db_connection():
    response = requests.get(f'{BASE_URL}/api/check_db_connection')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'

def test_get_message():
    response = requests.get(f'{BASE_URL}/api/message')
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Hello from Flask!'

def test_get_time():
    response = requests.get(f'{BASE_URL}/api/time')
    assert response.status_code == 200
    data = response.json()
    assert 'time' in data

def test_get_status():
    response = requests.get(f'{BASE_URL}/api/status')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'Everything is running smoothly!'

# def test_verify_timesheet():
#     payload = {
#         'email': 'test@example.com',
#         'tableData': [
#             {'date': '2024-07-20', 'role': 'Developer', 'position': 'Full-Time', 'hours': 8},
#             {'date': '2024-07-21', 'role': 'Tester', 'position': 'Part-Time', 'hours': 4}
#         ]
#     }
#     response = requests.post(f'{BASE_URL}/verify', json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     assert 'report' in data
#     assert 'invalidEntries' in data

email = "abdel.nasser045@gmail.com"
def test_api():
    api_url = os.getenv('API_URL', 'http://backend:5001/verify')  # Use the service name 'backend'
    data = {
        "email": email,
        "tableData": [             
                    {"date": '2023-12-03', "hours": 2.25, "location": 'Good Shepherd ', "position": 'Teacher - Lead'} ,            
                    {"date": '2023-12-04', "hours": 2, "location": 'Oakland Terrace ES', "position": 'Teacher - Lead'},                
                    {"date": '2023-12-05', "hours": 2.75, "location": 'Burning Tree ES', 'position': 'Teacher - Assistant'},
                    {"date": '2023-12-06', "hours": 2.5, "location": 'Forest knolls ES', "position": 'Teacher - Lead'} ,
                    {"date": '2023-12-11', "hours": 2.5, "location": 'ST andrew', "position": 'Teacher - Lead'},
        ]
    }

    try:
        response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        if response.status_code == 200:
            print("API Test Passed: Received 200 OK")
            print("Response:", response.json())
        else:
            print(f"API Test Failed: Received {response.status_code}")
            print("Response:", response.json())
    except Exception as e:
        print(f"API Test Failed: An error occurred: {e}")


