import unittest
from app import create_app, db
from app.models import Employee, Event

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the app wi th the testing configuration
        self.app = create_app('testing')        
        self.client = self.app.test_client()

        # Create all tables in the in-memory SQLite database
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_employee_model(self):
        # Create and add an employee to the database
        employee = Employee(name='John Doe', email='john.doe@example.com')
        with self.app.app_context():
            db.session.add(employee)
            db.session.commit()
            # Check if the employee count is 1
            self.assertEqual(Employee.query.count(), 1)

    def test_event_model(self):
        # Create an employee and an event, and add them to the database
        employee = Employee(name='John Doe', email='john.doe@example.com')
        event = Event(name='Meeting', date='2024-06-20', duration='1h', position='Manager', location='Office', employee=employee)
        with self.app.app_context():
            db.session.add(employee)
            db.session.add(event)
            db.session.commit()
            # Check if the event count is 1
            self.assertEqual(Event.query.count(), 1)

if __name__ == '__main__':
    unittest.main()
