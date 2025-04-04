def insert_data_to_postgresql(connection, data):
    """
    Insert data into a PostgreSQL table.

    :param connection: The PostgreSQL connection object.
    :param data: A list of dictionaries containing the data to insert.
    """
    try:
        with connection.cursor() as cursor:
            # Define the insert query
            insert_query = """
            INSERT INTO "User" (id, first_name, last_name, gender, email, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            inserted_count = 0

            # Iterate over the data and execute the query
            for record in data:
                cursor.execute(insert_query, (
                    str(record["_id"]),
                    record.get("firstName"),
                    record.get("lastName"),
                    record.get("gender"),
                    record.get("email"),
                    record.get("phoneNumber")
                ))
                inserted_count += 1

            # Commit the transaction
            connection.commit()
            print(f"Inserted {inserted_count} records into PostgreSQL successfully.")

    except Exception as e:
        print(f"Error inserting data into PostgreSQL: {e}")
        connection.rollback()