import pandas as pd
from sqlalchemy import create_engine, text

# --- Same MySQL connection details as before ---
MYSQL_USER = "root"          # or "sana" if you created that user
MYSQL_PASSWORD = "12345"
MYSQL_HOST = "localhost"
MYSQL_DB = "ecommerce_db"

from db_connection import engine

# --- Words that should NEVER appear in a query we run ---
FORBIDDEN_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE", "REPLACE"]


def is_query_safe(sql_query: str) -> bool:
    """
    Checks that the SQL only contains a SELECT statement,
    and blocks anything that could modify or delete data.
    """
    sql_upper = sql_query.strip().upper()

    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return False

    # Must not contain any dangerous keywords anywhere in the query
    for word in FORBIDDEN_KEYWORDS:
        if word in sql_upper:
            return False

    return True


def execute_query(sql_query: str):
    """
    Runs the SQL query safely against MySQL and returns results as a DataFrame.
    Returns an error message (string) if the query is unsafe or fails.
    """
    if not is_query_safe(sql_query):
        return "BLOCKED: This query contains unsafe or disallowed operations. Only SELECT statements are permitted."

    try:
        with engine.connect() as conn:
            result_df = pd.read_sql(text(sql_query), conn)
        return result_df
    except Exception as e:
        return f"ERROR: Query failed to execute.\nDetails: {str(e)}"


# --- Quick test ---
if __name__ == "__main__":
    # Test 1: A safe query that should work
    safe_sql = "SELECT city, COUNT(*) as total FROM customers GROUP BY city LIMIT 5;"
    print("Testing safe query...")
    print(execute_query(safe_sql))

    print("\n" + "=" * 60 + "\n")

    # Test 2: A dangerous query that should get blocked
    unsafe_sql = "DROP TABLE customers;"
    print("Testing unsafe query...")
    print(execute_query(unsafe_sql))