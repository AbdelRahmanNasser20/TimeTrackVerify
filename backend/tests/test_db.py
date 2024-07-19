import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from app import create_app, db
from app.models import Employee, Event

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

@pytest.fixture(scope='module')
def app():
    print("Setting up the Flask application")
    app = create_app('testing')
    with app.app_context():
        yield app
    print("Teardown the Flask application")

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def database(app):
    print("Setting up the database")
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], connect_args={"connect_timeout": 10})
    Session = sessionmaker(bind=engine)
    session = Session()
    with app.app_context():
        db.create_all()
        inspector = inspect(engine)
        print("Tables created:", inspector.get_table_names())
        yield session
        db.session.remove()
        db.drop_all()
    session.close()
    engine.dispose()
    print("Teardown the database")

def test_db_connection(database):
    print("Testing database connection")
    try:
        result = database.execute(text('SELECT 1')).scalar()
        assert result == 1
        print("Database connection test completed")
    except Exception as e:
        print(f"Exception occurred during database connection test: {e}")
        raise

def test_insert_employee(database):
    print("Testing insert employee")
    try:
        employee = Employee(name='John Doe', email='john.doe@example.com')
        print("Created employee:", employee)
        database.add(employee)
        print("Added employee to session")
        database.commit()
        print("Committed employee to database")
        result = database.query(Employee).filter_by(email='john.doe@example.com').first()
        print("Queried employee:", result)
        assert result is not None
        assert result.name == 'John Doe'
        print("Insert employee test completed")
    except Exception as e:
        print(f"Exception occurred during insert employee test: {e}")
        raise  # Reraise the exception to ensure it's noted
    finally:
        database.rollback()

def test_insert_event(database):
    print("Testing insert event")
    try:
        employee = Employee(name='John Doe', email='john.doe@example.com')
        print("Created employee:", employee)
        database.add(employee)
        database.commit()
        print("Committed employee to database")

        event = Event(
            name='Meeting', date='2024-06-20', duration='1h',
            position='Manager', location='Office', employee_id=employee.id
        )
        print("Created event:", event)
        database.add(event)
        database.commit()
        print("Committed event to database")

        result = database.query(Event).filter_by(name='Meeting').first()
        print("Queried event:", result)
        assert result is not None
        assert result.position == 'Manager'
        assert result.employee_id == employee.id
        print("Insert event test completed")
    except Exception as e:
        print(f"Exception occurred during insert event test: {e}")
        raise  # Reraise the exception to ensure it's noted
    finally:
        database.rollback()
