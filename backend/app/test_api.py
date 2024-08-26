# import os
# import requests
# import pytest

# # Ensure environment variables are set for testing
# os.environ['DATABASE_URL'] = 'postgresql://abdelnasser:greatness@db:5432/mydatabase'
# os.environ['FLASK_ENV'] = 'testing'

# BASE_URL = 'http://backend:5001'

# def test_db_connection():
#     response = requests.get(f'{BASE_URL}/check_db_connection')
#     assert response.status_code == 200
#     data = response.json()
#     assert data['status'] == 'success'

# def test_get_message():
#     response = requests.get(f'{BASE_URL}/api/message')
#     assert response.status_code == 200
#     data = response.json()
#     assert data['message'] == 'Hello from Flask!'

# def test_get_time():
#     response = requests.get(f'{BASE_URL}/api/time')
#     assert response.status_code == 200
#     data = response.json()
#     assert 'time' in data

# def test_get_status():
#     response = requests.get(f'{BASE_URL}/api/status')
#     assert response.status_code == 200
#     data = response.json()
#     assert data['status'] == 'Everything is running smoothly!'

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
