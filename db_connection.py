import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="streamsphere_db",
        user="postgres",
        password="Streamsphere@123",
        port="5432"
    )