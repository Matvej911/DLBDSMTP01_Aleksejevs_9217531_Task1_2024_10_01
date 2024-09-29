import mysql.connector
from mysql.connector import Error
import os

def connect_to_database():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='db', 
            user=os.getenv('MYSQL_DB_USER'),
            password=os.getenv('MYSQL_ROOT_PASSWORD'),
            database='anomaly_detection'
        )
        if connection.is_connected():
            print("Connection to MySQL established successfully.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    """Close the MySQL connection."""
    if connection and connection.is_connected():
        connection.close()
        print("Connection to MySQL closed.")

if __name__ == "__main__":
    conn = connect_to_database()
    close_connection(conn)
