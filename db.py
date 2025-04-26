import psycopg2

def create_connection(db_name, user, password, host='localhost', port='5432'):
    """Create a database connection to the PostgreSQL database specified by db_name."""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connection to PostgreSQL DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")
    return conn

def execute_query(connection, query, params=None):
    """Execute a single query."""
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")
        connection.rollback()
    finally:
        cursor.close()

def execute_read_query(connection, query):
    """Execute a read query and return the results."""
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")
        return None
    
def main():
    connection = create_connection("railway", "postgres", "yfLEbMTMbRbtCHlYNEYONhvKYxsznzoA", "switchback.proxy.rlwy.net", "45837")

    query = """CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    datetime TIMESTAMP NOT NULL
);
"""

    res = execute_query(connection, query)

    if res:
        for row in res:
            print(row)
    

if __name__ == "__main__":
    main()