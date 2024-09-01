import pytest
from sqlalchemy import inspect, text

def test_db_connection(session):
    """Test that the database connection is established successfully."""
    try:
        connection = session.connection()
        assert connection is not None, "Failed to establish database connection"
        print("Success: Database connection established.")
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_tables_exist(session):
    """Test that all expected tables exist in the database."""
    try:
        inspector = inspect(session.bind)        
        tables = inspector.get_table_names()
        
        # Define the expected tables in your database
        expected_tables = {"alembic_version", "user", "events", "employees"}
        
        # Check if all expected tables are present
        missing_tables = expected_tables - set(tables)
        assert not missing_tables, f"Missing tables: {missing_tables}"
        print("Success: All expected tables exist in the database.")
    except Exception as e:
        pytest.fail(f"Failed to verify table existence: {e}")

def test_table_employees(session):
    """Test that the 'employees' table exists and can be queried."""
    try:
        inspector = inspect(session.bind)
        assert 'employees' in inspector.get_table_names(), "The 'employees' table does not exist"
        
        # Use the text() construct to execute the raw SQL query
        result = session.execute(text("SELECT COUNT(*) FROM employees")).scalar()
        assert result is not None, "Failed to query the 'employees' table"
        print("Success: 'employees' table exists and can be queried.")
    except Exception as e:
        pytest.fail(f"Failed to verify or query the 'employees' table: {e}")

def test_environment_variables(app):
    """Test and print all environment variables and validate essential ones based on the environment."""
    
    import os        
    flask_env = os.getenv('FLASK_ENV', 'development')

    if flask_env == 'development':
        assert os.getenv('FLASK_ENV') == 'development', "FLASK_ENV should be set to 'development'"
        assert os.getenv('DEBUG') == 'True', "DEBUG should be 'True' in development"
        assert os.getenv('DATABASE_URL'), "DATABASE_URL should be set in development"
        print("Success: Development environment variables are correctly set.")
    
    elif flask_env == 'production':
        assert os.getenv('FLASK_ENV') == 'production', "FLASK_ENV should be set to 'production'"
        # assert os.getenv('DEBUG') == 'False', "DEBUG should be 'False' in production"
        assert os.getenv('DOCKER_DATABASE_URL'), "HEROKU_DATABASE_URL should be set in production"
        
        print("Success: Production environment variables are correctly set.")
    
    elif flask_env == 'testing':
        assert os.getenv('FLASK_ENV') == 'testing', "FLASK_ENV should be set to 'testing'"
        assert os.getenv('TESTING') == 'True', "TESTING should be 'True' in testing"
        assert os.getenv('DATABASE_URL'), "DATABASE_URL should be set in testing"
        print("Success: Testing environment variables are correctly set.")
    
    else:
        pytest.fail(f"Unknown FLASK_ENV: {flask_env}")
    
