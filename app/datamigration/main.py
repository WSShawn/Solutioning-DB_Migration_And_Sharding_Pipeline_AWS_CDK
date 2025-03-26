# def handler(event, context):
#     return {"statusCode": 200, "body": "Hello from Data Migration Lambda!"}

from pymongo import UpdateOne
from helpers.connect_to_docdb import connect_to_docdb
from helpers.get_docdb_credentials import get_docdb_credentials
from helpers.shard_documents import shard_documents
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
		
		db = client['DBMigrationNShardingRaw']
		collection = db['ECommerceRawData']
		
		result_documents = shard_documents(collection)
		update_operations = []

		# If there are any updates to perform, execute them in bulk
		for idx, doc in enumerate(result_documents):
			print(f"Document {idx + 1} for migration:", doc)
			# Prepare an update operation to set the toBeMigrated flag to False
			update_operations.append(UpdateOne(
				{"_id": doc["_id"]},  # Use the unique identifier for the document
				{"$set": {"toBeMigrated": False}}
			))
		
		# If there are any updates to perform, execute them in bulk
		if update_operations:
			result = collection.bulk_write(update_operations)
			print(f"Updated {result.modified_count} documents to set toBeMigrated = False.")
	except Exception as e:
		print("Application error:", e)
	
	finally:
		if 'client' in locals() and client:
			client.close()
			print("Connection closed")
			

if __name__ == "__main__":
    main()
	
    
