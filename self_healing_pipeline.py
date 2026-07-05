from nl_to_sql import generate_sql, fix_sql
from query_executor import execute_query
import pandas as pd

MAX_RETRIES = 3


def ask_database_with_retry(user_question: str):
    print(f"\nQuestion: {user_question}")

    # First attempt
    sql = generate_sql(user_question)
    print(f"Attempt 1 - Generated SQL:\n{sql}\n")

    result = execute_query(sql)

    attempt = 1
    while isinstance(result, str) and result.startswith("ERROR") and attempt < MAX_RETRIES:
        attempt += 1
        print(f"Query failed. Retrying (attempt {attempt})...")
        print(f"Error was: {result}\n")

        # Ask the LLM to fix its own mistake
        sql = fix_sql(user_question, sql, result)
        print(f"Attempt {attempt} - Corrected SQL:\n{sql}\n")

        result = execute_query(sql)

    # Final outcome
    if isinstance(result, str):
        print("Failed after all retry attempts.")
        print(f"Last error: {result}")
    else:
        print("Success! Result:")
        print(result)

    return result


# --- Test it ---
if __name__ == "__main__":
    ask_database_with_retry("Show me all customers from Chicago")
    ask_database_with_retry("Which region has the highest profit?")
    ask_database_with_retry("What's the average delay in shipment across all orders?")
    ask_database_with_retry("Show me customers who never had a late delivery")