import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models import Employee, Event
from app.db_queries import (
    count_entries_for_employee,
    sum_hours_by_role_from_db,
    get_employee_id,
    get_events_for_employee_by_date
)

class TestDbQueries(TestCase):

    def create_app(self):
        # Pass in test configuration
        app = create_app('testing')
        return app

    def setUp(self):
        # Create the database and the database table
        db.create_all()

        # Insert test data
        employee = Employee(name='John Doe', email='john.doe@example.com')
        event1 = Event(
            name='Meeting', date='2024-06-20', duration='1.0',
            position='Manager', location='Office', employee=employee
        )
        event2 = Event(
            name='Workshop', date='2024-06-21', duration='2.5',
            position='Teacher', location='Conference Room', employee=employee
        )
        db.session.add(employee)
        db.session.add(event1)
        db.session.add(event2)
        db.session.commit()

    def tearDown(self):
        # Drop the database tables and remove the session
        db.session.remove()
        db.drop_all()

    def test_count_entries_for_employee(self):
        count = count_entries_for_employee(1)  # Assuming the employee ID is 1
        self.assertEqual(count, 2)

    def test_sum_hours_by_role_from_db(self):
        hours_by_role = sum_hours_by_role_from_db(1)  # Assuming the employee ID is 1
        self.assertEqual(hours_by_role['Manager'], 1.0)
        self.assertEqual(hours_by_role['Teacher'], 2.5)

    def test_get_employee_id(self):
        employee_id = get_employee_id('john.doe@example.com')
        self.assertIsNotNone(employee_id)
        self.assertEqual(employee_id, 1)  # Assuming the employee ID is 1

    def test_get_events_for_employee_by_date(self):
        event = get_events_for_employee_by_date(1, '2024-06-20')  # Assuming the employee ID is 1
        self.assertIsNotNone(event)
        self.assertEqual(event.name, 'Meeting')
        self.assertEqual(event.position, 'Manager')

if __name__ == '__main__':
    unittest.main()
