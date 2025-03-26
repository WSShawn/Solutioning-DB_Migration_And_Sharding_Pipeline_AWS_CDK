from pymongo import MongoClient
import ssl

def connect_to_docdb(credentials):   
    # Establish the connection to DocumentDB
    if not credentials:
        print("No credentials provided")
        return None
        
    try:
        client = MongoClient("mongodb://docdbadmin:Apply2025!@docdbclusterinstance15e47fa-0etykuhor6oj.ck1k80ayiam1.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=%2FUsers%2Fyumeng%2FDesktop%2FPersonalProjects%2Fglobal-bundle.pem&retryWrites=false&readPreference=nearest", ssl=True)
        client.admin.command('ping')
        print("Connected to DocumentDB!")

        # Sample operation: List databases
        databases = client.list_database_names()
        print("Available Databases:", databases)
        return client

    except Exception as e:
        print("An error occurred while connecting to DocumentDB:", e)
        return None