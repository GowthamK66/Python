import pandas as pd
from sqlalchemy import create_engine, event
import time
import glob
import os
import csv

def format_time(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))  #changed "%M:%S"

# Start the overall timing
overall_start_time = time.time()

# Define Azure SQL Database connection details
server = '***'
database = '***'
username = '***'
password = '***'

# Create the SQLAlchemy engine with connection string
connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
engine = create_engine(connection_string, echo=True)

# Define event listener for before cursor execution
@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if executemany:
        cursor.fast_executemany = True

# Check if the table already exists
start_time = time.time()
with engine.connect() as conn, conn.begin():
    cursor = conn.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'RMSSAMPLE' AND TABLE_NAME = 'Python_Script_12'")
    if cursor.fetchone()[0] == 0:
        # Table does not exist, create it
        cursor.execute(
            """
            CREATE TABLE [RMSSAMPLE].[Python_Script_12]
            (
            Time_Period_s_Weekly nvarchar(50),
            Category nvarchar(50),
            Sub_Category nvarchar(50),
            Glue_Hierarcy_II nvarchar(50),
            Writing_Classification nvarchar(50),
            Brand nvarchar(50),
            Model_Number nvarchar(max),
            Item_Description nvarchar(max),
            Outlet_Family nvarchar(50),
            Outlet nvarchar(50),
            Dollars bigint,
            Units int
            )
            """
        )
        cursor.commit()
        print("Table created successfully!")
    else:
        print("Table already exists!")
elapsed_time = time.time() - start_time
print(f"Table check and creation took {format_time(elapsed_time)} (HH:MM:SS).")   #Changed (MM:SS)

# Check the data is already available in the SQL table (to avoid duplication)
start_time = time.time()
AA = cursor.execute("SELECT COUNT(*) FROM [RMSSAMPLE].[Python_Script_12]")
count = AA.fetchone()[0]
elapsed_time = time.time() - start_time
print(f"Data existence check took {format_time(elapsed_time)} (HH:MM:SS).")   #Changed (MM:SS)
if count == 0:
    # Pick the folder from local
    file_path = r'C:\Users\iv14822\OneDrive - Newell Brands\Desktop\Bulk_12_Insert_col'
    file_extension = 'csv'
    
    csv_files = glob.glob(file_path + '/*.' + file_extension)

    # Check if all CSV files have the same number of columns and column names
    num_columns = None
    consistent_column_names = True

    start_time = time.time()
    for csv_file in csv_files:
        # Read the first row of the CSV file to get the column names
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            column_names = next(reader)
            
        # Check if the number of columns matches
        if num_columns is None:
            num_columns = len(column_names)
        elif len(column_names) != num_columns:
            print(f"The File ---->'{os.path.basename(csv_file)}' has a different number of columns.")
            consistent_column_names = False
            break
    elapsed_time = time.time() - start_time
    print(f"Column consistency check took {format_time(elapsed_time)} (HH:MM:SS).")   #Changed (MM:SS)

    # If columns are consistent, proceed with data insertion
    if consistent_column_names:
        chunk_size = 30000
        total_rows_inserted = 0

        start_time = time.time()
        for csv_file in csv_files:
            for chunk in pd.read_csv(csv_file, dtype={'Model_Number': str}, chunksize=chunk_size):
                chunk.to_sql('Python_Script_12', engine, index=False, if_exists="append", schema="RMSSAMPLE")
                total_rows_inserted += len(chunk)
                print(f"Inserted {total_rows_inserted} rows so far.")
        elapsed_time = time.time() - start_time
        print(f"CSV files reading and insertion in chunks took {format_time(elapsed_time)} (HH:MM:SS).")   #Changed (MM:SS)
    else:
        print("Columns in CSV files are not consistent. Please check the files.")

# Print the overall time taken for the script
elapsed_time = time.time() - overall_start_time
print(f"Overall script execution took {format_time(elapsed_time)} (HH:MM:SS).")   #Changed (MM:SS)
