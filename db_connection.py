import mysql.connector

def get_db_connection():
    """
    Establishes a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL host
            user="root",       # Replace with your MySQL username
            password="Nk258627",  # Replace with your MySQL password
            database="ehr_db",  # Replace with your database name
            buffered=True  # Enable buffered mode
        )
        # Test the connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("Database connection successful!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None