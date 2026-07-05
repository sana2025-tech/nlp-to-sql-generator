from nl_to_sql import generate_sql
from query_executor import execute_query


def ask_database(user_question: str):
    print(f"\nQuestion: {user_question}")

    sql = generate_sql(user_question)
    print(f"Generated SQL:\n{sql}\n")

    result = execute_query(sql)
    print("Result:")
    print(result)
    return result


# --- Test the full pipeline ---
if __name__ == "__main__":
    ask_database("Show me all customers from Chicago")
    ask_database("What is the total sales for each category?")
    ask_database("Which region has the highest profit?")