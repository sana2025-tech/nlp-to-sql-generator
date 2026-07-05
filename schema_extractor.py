from sqlalchemy import create_engine, inspect
import os

# --- Connect to your MySQL database ---
MYSQL_USER = "root"          # or "sana" if you created that user
MYSQL_PASSWORD = "12345"
MYSQL_HOST = "localhost"
MYSQL_DB = "ecommerce_db"

from db_connection import engine
inspector = inspect(engine)


def get_schema_text():
    """
    Reads all tables, columns, data types, and foreign keys
    from the MySQL database and returns it as a clean text block.
    """
    schema_lines = []
    tables = inspector.get_table_names()

    for table in tables:
        schema_lines.append(f"Table: {table}")

        # Columns + data types
        columns = inspector.get_columns(table)
        for col in columns:
            schema_lines.append(f"  - {col['name']} ({col['type']})")

        # Primary key
        pk = inspector.get_pk_constraint(table)
        if pk and pk.get("constrained_columns"):
            schema_lines.append(f"  Primary Key: {', '.join(pk['constrained_columns'])}")

        # Foreign keys
        fks = inspector.get_foreign_keys(table)
        for fk in fks:
            local_col = fk["constrained_columns"][0]
            ref_table = fk["referred_table"]
            ref_col = fk["referred_columns"][0]
            schema_lines.append(f"  Foreign Key: {local_col} -> {ref_table}.{ref_col}")

        schema_lines.append("")  # blank line between tables

    return "\n".join(schema_lines)


# --- Run and print the schema ---
if __name__ == "__main__":
    schema_text = get_schema_text()
    print(schema_text)

    # Save it to a file too, so we can reuse it later without re-querying
    with open("schema.txt", "w") as f:
        f.write(schema_text)

    print("\nSchema saved to schema.txt")