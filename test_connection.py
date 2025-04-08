from db_connection import get_db_connection

def test_db_connection():
    print("1. Starting database connection test...")
    connection = get_db_connection()

    if connection is None:
        print("2. Failed to connect to the database. Please check your MySQL server and credentials.")
    else:
        print("2. Database connection successful!")
        connection.close()

if __name__ == "__main__":
    print("0. Running the test script...")
    test_db_connection()
    print("3. Test script completed.")