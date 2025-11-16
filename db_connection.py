import psycopg2

# --- Database Connection ---
def get_db_connection(db_name, user, password, host="localhost", port=5432):
    print("db ",db_name, user, password)
    return psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )