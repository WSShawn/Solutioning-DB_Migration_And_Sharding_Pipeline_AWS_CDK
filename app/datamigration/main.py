# def handler(event, context):
#     return {"statusCode": 200, "body": "Hello from Data Migration Lambda!"}

from helpers.connect_to_docdb import connect_to_docdb
from helpers.get_docdb_credentials import get_docdb_credentials
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
	try:
		credentials = get_docdb_credentials()
		if not credentials:
			print("Failed to retrieve credentials")
			return

		client = connect_to_docdb(credentials)

		if not client:
			print("Failed to connect to DocumentDB")
			return

	except Exception as e:
		print("Application error:", e)
	finally:
		if 'client' in locals() and client:
			client.close()
			print("Connection closed")

if __name__ == "__main__":
    main()
