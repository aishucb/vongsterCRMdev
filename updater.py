import mysql.connector
from pymongo import MongoClient

# MySQL Database credentials
mysql_db_config = {
    'host': '127.0.0.1',
    'user': 'vongle',
    'password': 'ashiv3377',
    'database': 'osqacademy',
}

# MongoDB credentials
mongo_uri = "mongodb+srv://vongmeetings2:LexW0wMXLOc2PRb5@cluster0.afg1ajm.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client.get_database("Vongdata")
mongo_collection = mongo_db.get_collection("test3")  # Update with the actual collection name

# File to store results
output_file = "result.txt"

try:
    # Establish a connection to the MySQL server
    mysql_connection = mysql.connector.connect(**mysql_db_config)

    if mysql_connection.is_connected():
        print("Connected to MySQL database")

        # Create a cursor object to execute SQL queries
        cursor = mysql_connection.cursor()

        # Execute a SELECT query to get the list of documents from MongoDB
        mongo_documents = mongo_collection.find()

        # Open the file in append mode
        with open(output_file, "a") as result_file:
            # Iterate through each document in MongoDB
            for document in mongo_documents:
                username = document.get("full_name")
                user_id = document.get("roll_number")
                firstname = document.get("firstname")
                lastname = document.get("lastname")
                email = document.get("email")
                phone1 = document.get("phone")
                address = document.get("address")
                city = document.get("city")
                institution = document.get("institution")
                status = document.get("active")
                house = document.get("house")

                # Check if the user exists in MySQL
                query = "SELECT id FROM mdl_user WHERE username = %s"
                cursor.execute(query, (username,))
                user_exists = cursor.fetchone()

                if user_exists:
                    print(f"Record found in MySQL for username {username}")
                    result_file.write(f"Record found for username {username}\n")

                    # Update the record in MySQL
                    update_query = (
                        "UPDATE mdl_user SET id = %s, firstname = %s, lastname = %s, email = %s, "
                        "phone1 = %s, address = %s, city = %s, institution = %s, lastnamephonetic = %s, firstnamephonetic = %s "
                        "WHERE username = %s"
                    )
                    cursor.execute(
                        update_query,
                        (user_id, firstname, lastname, email, phone1, address, city, institution, status, house, username)
                    )
                    mysql_connection.commit()

                else:
                    print(f"No record found in MySQL for username {username}")
                    result_file.write(f"No record found for username {username}\n")

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection for MySQL
    if 'cursor' in locals():
        cursor.close()
    if 'mysql_connection' in locals() and mysql_connection.is_connected():
        mysql_connection.close()
        print("MySQL Connection closed")

    # Close the connection for MongoDB
    if 'mongo_client' in locals():
        mongo_client.close()
        print("MongoDB Connection closed")
