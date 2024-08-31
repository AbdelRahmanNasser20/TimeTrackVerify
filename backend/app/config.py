import os

dev_database = "postgresql://abdelnasser:greatness@localhost:5432/mydatabase"

class Config:
    """Base configuration with default settings."""    
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', dev_database)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True

class DevelopmentConfig(Config):
    """Development configuration with additional debugging and testing features."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', dev_database)
    

class ProductionConfig(Config):
    """Production configuration with settings optimized for performance and security."""
    SQLALCHEMY_DATABASE_URI = os.getenv('HEROKU_DATABASE_URL', dev_database)    

class TestingConfig(Config):
    """Testing configuration with settings optimized for testing."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    # 'production': ProductionConfig
}