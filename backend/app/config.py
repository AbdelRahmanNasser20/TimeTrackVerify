import os

default_database = "postgresql://abdelnasser:greatness@localhost:5432/mydatabase"
test_database = "postgresql://abdelnasser:greatness@localhost:5432/mydatabase_test"

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default_database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration with additional debugging and testing features."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', default_database)

class TestingConfig(Config):
    """Testing configuration with settings optimized for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', test_database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration with settings optimized for performance and security."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default_database)
    DEBUG = False
    TESTING = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
