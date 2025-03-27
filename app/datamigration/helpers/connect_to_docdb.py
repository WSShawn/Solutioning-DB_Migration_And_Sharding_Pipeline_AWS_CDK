from pymongo import MongoClient
import os
import ssl

def connect_to_docdb(credentials):   
    # Establish the connection to DocumentDB
    if not credentials:
        print("No credentials provided")
        return None

    try:
        # Dynamically construct the path to the .pem file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pem_file_path = os.path.join(current_dir, "global-bundle.pem")

        # Verify the .pem file exists
        if not os.path.exists(pem_file_path):
            print(f"Certificate file not found: {pem_file_path}")
            return None

        # Construct the connection string using credentials
        username = credentials.get("username", "docdbadmin")
        password = credentials.get("password", "Apply2025!")
        host = credentials.get("host", "docdbclusterinstance15e47fa-0etykuhor6oj.ck1k80ayiam1.us-east-1.docdb.amazonaws.com")
        port = credentials.get("port", 27017)

        connection_string = f"mongodb://{username}:{password}@{host}:{port}/?tls=true&retryWrites=false&readPreference=nearest"

        # Connect to DocumentDB
        client = MongoClient(connection_string, tls=True, tlsCAFile=pem_file_path)
        client.admin.command('ping')
        print("Connected to DocumentDB!")

        # Sample operation: List databases
        databases = client.list_database_names()
        print("Available Databases:", databases)
        return client

    except Exception as e:
        print("An error occurred while connecting to DocumentDB:", e)
        return None