import os
import sys
import pytest
from dotenv import load_dotenv
from app import create_app, db as _db
from sqlalchemy.orm import scoped_session, sessionmaker

# Ensure the sys.path includes the backend directory for imports
from dotenv import load_dotenv
load_dotenv()

@pytest.fixture(scope='session')
def app():
    """Setup Flask application for testing."""

    flask_env = os.getenv('FLASK_ENV')
    # Use the 'testing' configuration or whichever is appropriate
    if flask_env == 'testing':        
        # For testing, use SQLite in-memory database
        app = create_app('testing')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        # Otherwise, use the specified environment (development, production)
        app = create_app(flask_env)
    
    with app.app_context():
        yield app  # This is where the testing happens

@pytest.fixture(scope='session')
def db(app):
    """Setup the database for testing."""
    _db.app = app
    _db.create_all()

    yield _db  # Provide the fixture value

    # _db.session.remove()
    # if app.config['TESTING']:
    #     print("**********************/////////////////WARNING DROPING ALLL TABLES*********************//////////////////")
    #     _db.drop_all()  # Only drop tables if in testing mode

@pytest.fixture(scope='function')
def session(db):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    # Use sessionmaker to create a new session
    session = scoped_session(sessionmaker(bind=connection))

    yield session  # This is where the test runs

    transaction.rollback()
    connection.close()
    session.remove()