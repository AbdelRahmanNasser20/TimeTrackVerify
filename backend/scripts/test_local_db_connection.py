import os
import argparse
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Function to get the database URL based on the environment
def get_database_url():
    # Check the environment variable
    environment = os.getenv("ENVIRONMENT", "localhost")
    
    return "postgresql://abdelnasser:greatness@127.0.0.1:5432/mydatabase"
    if environment == "production":
        # Assuming the PostgreSQL service is named "db" in Docker
        return "postgresql://abdelnasser:greatness@db:5432/mydatabase"
        
    else:
        # Default to localhost if not running in Docker
        return "postgresql://abdelnasser:greatness@localhost:5432/mydatabase"

# Function to allow overriding with command line arguments
def parse_arguments():
    default_url = get_database_url()
    
    parser = argparse.ArgumentParser(description="Connect to a PostgreSQL database and print the first 10 rows of each table.")
    parser.add_argument(
        "database_url",
        nargs="?",
        default=default_url,
        help=f"Database URL (default: {default_url})"
    )
    
    args = parser.parse_args()
    return args.database_url

# Main function to connect to the database and print the first 10 rows of each table
def main():
    # Get the database URL
    database_url = parse_arguments()

    # Create the engine
    engine = create_engine(database_url)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Reflect the tables
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Get a list of all table names
    tables = metadata.tables.keys()

    for table_name in tables:
        print(f"\nTable: {table_name}")
        
        # Reflect each table
        table = Table(table_name, metadata, autoload_with=engine)
        
        # Perform a select to fetch the first 10 rows
        query = table.select().limit(10)
        result = session.execute(query)
        
        # Print the first 10 rows
        for row in result.fetchall():
            print(row)

    # Close the session
    session.close()

if __name__ == "__main__":
    main()