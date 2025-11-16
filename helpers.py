import re
import json
from typing import Optional
import psycopg2


def extract_sql_query(response_bytes: bytes) -> Optional[str]:
    """
    Extracts the SQL query from a model response.

    Args:
        response_bytes (bytes): The raw response from the model (JSON encoded).

    Returns:
        Optional[str]: The extracted SQL query if found, else None.
    """
    try:
        # Decode bytes to string
        response_str = response_bytes.decode('utf-8')

        # Load JSON
        data = json.loads(response_str)

        # Get the "response" field
        response_text = data.get("response", "")

        # Try to extract SQL code block
        match = re.search(r"```sql\n(.*?)\n```", response_text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Fallback: try to find a SQL statement in plain text
        # Simple regex to capture SELECT/INSERT/UPDATE/DELETE statements
        fallback_match = re.search(r"(SELECT|INSERT|UPDATE|DELETE).*?;", response_text, re.IGNORECASE | re.DOTALL)
        if fallback_match:
            return fallback_match.group(0).strip()

        # If nothing found
        return None

    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Error parsing response: {e}")
        return None


# SQL PASER
def sql_parser(sql: str, db_name, user, password, host="localhost", port=5432) -> bool:
    try:
        conn = psycopg2.connect(f"dbname={db_name} user={user} password={password} host={host} port={port}")
        conn.autocommit = False
        cur = conn.cursor()
        cur.execute(sql)
        conn.rollback()
        return True
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return False