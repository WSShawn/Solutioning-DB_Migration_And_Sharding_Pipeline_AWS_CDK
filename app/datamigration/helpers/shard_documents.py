
from pymongo import MongoClient

def shard_documents(collection):
    # Initialize a list to hold batches of documents
    shard_documents = []
    client = MongoClient("mongodb://docdbadmin:Apply2025!@docdbclusterinstance15e47fa-0etykuhor6oj.ck1k80ayiam1.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=%2FUsers%2Fyumeng%2FDesktop%2FPersonalProjects%2Fglobal-bundle.pem&retryWrites=false&readPreference=nearest", ssl=True)
    db = client['DBMigrationNShardingRaw']
    collection = db['ECommerceRawData']
    documents = collection.find({"toBeMigrated": True})

    for document in documents:
        # Extract only the necessary fields if they exist
        if 'firstName' in document and 'lastName' in document and 'gender' in document and 'email' in document and 'phoneNumber' in document :
            # Include only the desired variables
            shard_documents.append({
                '_id': document['_id'],
                'firstName': document['firstName'],
                'lastName': document['lastName'],
                'gender': document['gender'],
                'email': document['email'],
                'phoneNumber': document['phoneNumber']
            })
    
    return shard_documents
        
    
