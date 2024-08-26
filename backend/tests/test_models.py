import pytest
from sqlalchemy import inspect
from app.models import Employee, Event, User  # Import your models here

def test_employee_model(db):
    """Test the Employee model schema."""
    inspector = inspect(db.engine)
    
    # Check that the 'employees' table exists
    assert 'employees' in inspector.get_table_names(), "'employees' table does not exist"
    
    # Check the columns in the 'employees' table
    columns = inspector.get_columns('employees')
    column_names = {column['name'] for column in columns}
    
    expected_columns = {'id', 'name', 'email', 'phone_number'}
    missing_columns = expected_columns - column_names
    assert not missing_columns, f"Missing columns in 'employees' table: {missing_columns}"

    print(f"Success: 'employees' table has the expected columns: {column_names}")

def test_event_model(db):
    """Test the Event model schema."""
    inspector = inspect(db.engine)
    
    # Check that the 'events' table exists
    assert 'events' in inspector.get_table_names(), "'events' table does not exist"
    
    # Check the columns in the 'events' table
    columns = inspector.get_columns('events')
    column_names = {column['name'] for column in columns}
    
    expected_columns = {'id', 'employee_id', 'name', 'date', 'duration', 'position', 'location'}
    missing_columns = expected_columns - column_names
    assert not missing_columns, f"Missing columns in 'events' table: {missing_columns}"

    print(f"Success: 'events' table has the expected columns: {column_names}")

def test_user_model(db):
    """Test the User model schema."""
    inspector = inspect(db.engine)
    
    # Check that the 'user' table exists
    assert 'user' in inspector.get_table_names(), "'user' table does not exist"
    
    # Check the columns in the 'user' table
    columns = inspector.get_columns('user')
    column_names = {column['name'] for column in columns}
    
    expected_columns = {'id', 'username', 'email'}
    missing_columns = expected_columns - column_names
    assert not missing_columns, f"Missing columns in 'user' table: {missing_columns}"

    print(f"Success: 'user' table has the expected columns: {column_names}")
