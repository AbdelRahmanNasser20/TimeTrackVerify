# scripts/__init__.py

import os

def get_database_uri():
    return os.getenv('DATABASE_URI')