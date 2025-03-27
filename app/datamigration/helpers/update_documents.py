from pymongo import UpdateOne

def update_documents(collection, result_documents):
    """
    Update the documents in the collection by setting the 'toBeMigrated' flag to False.

    Args:
        collection: The MongoDB collection object.
        result_documents: A list of documents to be updated.

    Returns:
        The result of the bulk write operation.
    """
    update_operations = []

    # Prepare update operations for each document
    for idx, doc in enumerate(result_documents):
        if "_id" not in doc:
            print(f"Skipping document {idx + 1} as it is missing the '_id' field:", doc)
            continue

        print(f"Document {idx + 1} for migration:", doc)
        update_operations.append(UpdateOne(
            {"_id": doc["_id"]},  # Use the unique identifier for the document
            {"$set": {"toBeMigrated": False}}
        ))

    # Execute the bulk write operation if there are updates
    if update_operations:
        result = collection.bulk_write(update_operations)
        print(f"Updated {result.modified_count} documents to set toBeMigrated = False.")
        return result
    else:
        print("No documents to update.")
        return None