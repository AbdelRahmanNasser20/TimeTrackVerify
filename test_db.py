from sqlalchemy import create_engine, inspect, text

def check_db_init():
    try:
        with engine.connect() as connection:
            # Use `text()` to wrap the raw SQL query
            result = connection.execute(text('SELECT 1')).scalar()
            if result == 1:
                print("Database connection is working.")
            else:
                print("Database connection failed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_table_existence(table_name):
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if table_name in tables:
            print(f"Table '{table_name}' exists.")
        else:
            print(f"Table '{table_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_table_columns(table_name):
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        if columns:
            print(f"Columns in table '{table_name}':")
            for column in columns:
                print(column['name'])
        else:
            print(f"No columns found for table '{table_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_all_entries_in_table(table_name):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name}"))
            rows = result.fetchall()
            if rows:
                print(f"Entries in table '{table_name}':")
                for row in rows:
                    print(row)
            else:
                print(f"No entries found in table '{table_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    
    # SQLALCHEMY_DATABASE_URI = 'postgresql://abdelnasser:greatness@localhost:5432/mydatabase'
    SQLALCHEMY_DATABASE_URI = "postgresql://u7rjm4v00r7o80:p29318c85fd890024aabb5af0d2eee671f3b489fceb0846bc261184455c66a610@cb5ajfjosdpmil.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dcbccjj9ki7jbl"

    # Create a SQLAlchemy engine
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    check_db_init()
    check_table_existence('employees')
    print_table_columns('employees')
    print_all_entries_in_table('employees')