from sqlalchemy import create_engine, text
import pandas as pd
import sys

# Connection info
server = '***'
database = '***'
username = '***'
password = '***'

# Connection string for SQLAlchemy using pyodbc
conn_str = f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# Create SQLAlchemy engine
engine = create_engine(conn_str)

try:
    with engine.connect() as conn:
        # Check if table has data
        result = conn.execute(text("SELECT COUNT(*) AS cnt FROM rmssample.testing"))
        count = result.scalar()
        print(count)

        if count > 0:
            print("Data already exists. Exiting.")
            sys.exit(0)
        else:
            print("Table is empty. Loading data...")

            # ✅ Load CSV into a DataFrame
            df = pd.read_csv(r"C:\Users\iv14822\OneDrive - Newell Brands\Desktop\tester.csv")

            # ✅ Insert DataFrame into SQL table
            df.to_sql('testing', con=engine, schema='rmssample', if_exists='replace', index=False)
            print("Data loaded successfully.")

except Exception as e:
    print("Error:", e)
