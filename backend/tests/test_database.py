import pytest
from sqlalchemy import inspect
from app.models import Employee  # Assuming your models are in app.models

def test_db_connection(db):
    """Test that the database connection is established successfully."""
    try:
        
        connection = db.engine.connect()
        assert connection is not None, "Failed to establish database connection"
        print("Success: Database connection established.")
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_tables_exist(db):
    """Test that all expected tables exist in the database."""
    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        # Define the expected tables in your database
        expected_tables = {"alembic_version", "user", "events", "employees"}
        
        # Check if all expected tables are present
        missing_tables = expected_tables - set(tables)
        assert not missing_tables, f"Missing tables: {missing_tables}"
        print("Success: All expected tables exist in the database.")
    except Exception as e:
        pytest.fail(f"Failed to verify table existence: {e}")

def test_table_employees(db):
    """Test that the 'employees' table exists and can be queried using SQLAlchemy ORM."""
    try:
        # Check if the 'employees' table exists by querying it with SQLAlchemy ORM
        employee_count = db.session.query(Employee).count()
        print(employee_count)
        assert employee_count > 0, "Failed to query the 'employees' table"
        print(f"Success: 'employees' table exists and has {employee_count} records.")
    except Exception as e:
        pytest.fail(f"Failed to verify or query the 'employees' table: {e}")