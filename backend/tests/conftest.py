import pytest
from app import create_app, db
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

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
        yield session
        db.session.remove()
        db.drop_all()
    session.close()
    engine.dispose()
    print("Teardown the database")


    