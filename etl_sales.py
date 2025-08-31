import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER", "sales_user")
DB_PASS = os.getenv("DB_PASS", "StrongPass123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "sales_db")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

df = pd.read_csv("sales.csv")

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df = df.dropna(subset=["order_id", "order_date"])
df["total_price"] = df["unit_price"] * df["quantity"] * (1 - df["discount"])
df["order_month"] = df["order_date"].dt.to_period('M').astype(str)

df.to_sql("sales", engine, if_exists="append", index=False)

print("✅ Data loaded successfully!")
