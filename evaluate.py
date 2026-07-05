import pandas as pd
from nl_to_sql import generate_sql, fix_sql
from query_executor import execute_query, engine
from test_questions import test_cases
from sqlalchemy import text

MAX_RETRIES = 3


def get_expected_result(expected_sql: str):
    """Runs the known-correct SQL and returns the DataFrame."""
    with engine.connect() as conn:
        return pd.read_sql(text(expected_sql), conn)


def results_match(actual_df, expected_df) -> bool:
    """
    Compares two DataFrames for equality, ignoring:
    - column name differences (e.g. 'total' vs 'total_sales')
    - row order differences
    """
    if not isinstance(actual_df, pd.DataFrame) or not isinstance(expected_df, pd.DataFrame):
        return False

    if actual_df.shape != expected_df.shape:
        return False

    # Sort values so row order doesn't matter, compare only the values (not column names)
    actual_sorted = actual_df.apply(lambda col: col.astype(str)).sort_values(by=list(actual_df.columns)).reset_index(drop=True)
    expected_sorted = expected_df.apply(lambda col: col.astype(str)).sort_values(by=list(expected_df.columns)).reset_index(drop=True)

    return actual_sorted.values.tolist() == expected_sorted.values.tolist()


def run_evaluation():
    total = len(test_cases)
    correct = 0
    results_log = []

    for i, case in enumerate(test_cases, start=1):
        question = case["question"]
        expected_sql = case["expected_sql"]

        # Get the correct answer
        expected_df = get_expected_result(expected_sql)

        # Run through your actual pipeline (with self-healing retries)
        generated_sql = generate_sql(question)
        actual_result = execute_query(generated_sql)

        attempt = 1
        while isinstance(actual_result, str) and actual_result.startswith("ERROR") and attempt < MAX_RETRIES:
            attempt += 1
            generated_sql = fix_sql(question, generated_sql, actual_result)
            actual_result = execute_query(generated_sql)

        is_correct = results_match(actual_result, expected_df)
        if is_correct:
            correct += 1

        status = "PASS" if is_correct else "FAIL"
        print(f"[{i}/{total}] {status} - {question}")

        results_log.append({
            "question": question,
            "status": status,
            "generated_sql": generated_sql
        })

    accuracy = (correct / total) * 100
    print("\n" + "=" * 50)
    print(f"FINAL ACCURACY: {correct}/{total} = {accuracy:.1f}%")
    print("=" * 50)

    # Save detailed results to a CSV for your README/portfolio
    pd.DataFrame(results_log).to_csv("evaluation_results.csv", index=False)
    print("\nDetailed results saved to evaluation_results.csv")

    return accuracy


if __name__ == "__main__":
    run_evaluation()