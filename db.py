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
    except Exception as e:
        print(f"The error '{e}' occurred")
        connection.rollback()
    finally:
        cursor.close()

def execute_read_query(connection, query, params=None):
    """Execute a read query and return the results."""
    cursor = connection.cursor()
    result = None
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")
        return None