from helpers.connect_to_docdb import connect_to_docdb
from helpers.get_docdb_credentials import get_docdb_credentials
from helpers.shard_documents import shard_documents
from helpers.update_documents import update_documents
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """
    Main function to handle the data migration and sharding process.
    """
    try:
        # Step 1: Retrieve DocumentDB credentials
        credentials = get_docdb_credentials()
        if not credentials:
            print("Failed to retrieve credentials")
            return

        # Step 2: Connect to DocumentDB
        client = connect_to_docdb(credentials)
        if not client:
            print("Failed to connect to DocumentDB")
            return

        # Step 3: Access the database and collection
        db = client['DBMigrationNShardingRaw']
        collection = db['ECommerceRawData']

        # Step 4: Shard documents and prepare for migration
        result_documents = shard_documents(collection)

        # Step 5: Update documents in the collection
        update_documents(collection, result_documents)

    except Exception as e:
        # Handle any application errors
        print("Application error:", e)

    finally:
        # Ensure the client connection is closed
        if 'client' in locals() and client:
            client.close()
            print("Connection closed")

if __name__ == "__main__":
    main()