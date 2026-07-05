import os
from sqlalchemy import create_engine

# Set this to "sqlite" for deployment, "mysql" for local development
DB_MODE = os.environ.get("DB_MODE", "sqlite")

if DB_MODE == "mysql":
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_DB = os.environ.get("MYSQL_DB", "ecommerce_db")
    engine = create_engine(
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}?use_pure=true",
        pool_pre_ping=True
    )
else:
    engine = create_engine("sqlite:///ecommerce.db")