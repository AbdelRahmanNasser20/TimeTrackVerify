from sqlalchemy import create_engine, inspect

def check_db_init():
    try:
        with engine.connect() as connection:
            result = connection.execute('SELECT 1').scalar()
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
            result = connection.execute(f"SELECT * FROM {table_name}")
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
    
    DATABASE_URL = 'postgresql://abdelnasser:greatness@db:5432/mydatabase'
    # Create a SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    check_db_init()
    # check_table_existence('employees')
    # print_table_columns('employees')
    # print_all_entries_in_table('employees')