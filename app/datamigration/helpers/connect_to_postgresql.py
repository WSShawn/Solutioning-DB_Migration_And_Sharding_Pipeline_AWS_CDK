import psycopg2
from psycopg2 import sql, OperationalError

# Predefined connection parameters
ENDPOINT = "postgresql.ck1k80ayiam1.us-east-1.rds.amazonaws.com"
PORT = 5432  # Replace with your port if different
DATABASE = "postgres"
USER = "postgresadmin"
PASSWORD = "={+1*6<>#(20N|BaJ\*v&cpb[?c`kzS["

def connect_to_postgresql():
    """
    Connect to a PostgreSQL database using predefined connection parameters.

    :return: A connection object if successful, None otherwise
    """
    try:
        connection = psycopg2.connect(
            host=ENDPOINT,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        print("Connection to PostgreSQL database successful")
        return connection
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None