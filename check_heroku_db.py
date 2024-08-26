import psycopg2
from psycopg2 import OperationalError

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database="de7v5q4eis0spk",
            user="u6lschcv17405e",
            password="p75d078e37eed9766afac5114f6026bbf9533d2b6b0b0d038fbcdae3518da298c",
            host="caij57unh724n3.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
            # database="mydatabase",
            # user="abdelnasser",
            # password="greatness",
            # host="127.0.0.1",
            port="5432",
            connect_timeout=10  # Timeout after 10 seconds
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

if __name__ == "__main__":
    connection = create_connection()

    if connection:
        connection.close()
        print("Connection closed")