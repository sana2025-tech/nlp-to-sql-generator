import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# Connect to your existing SQLite database
sqlite_conn = sqlite3.connect(r'C:\Users\sb948\Downloads\ecommerce.db')

# Create a SQLAlchemy engine for MySQL (this is what to_sql actually needs)
mysql_engine = create_engine("mysql+mysqlconnector://root:12345@localhost/ecommerce_db")

tables = ["categories", "products", "customers", "orders", "order_items"]

for t in tables:
    df = pd.read_sql(f"SELECT * FROM {t}", sqlite_conn)
    df.to_sql(t, mysql_engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into {t}")

print("All tables loaded successfully into MySQL!")