import sqlite3
import os

# Define the database path
db_path = os.path.join(os.path.abspath('instance'), 'election.db')

# Verify the path
print(f"Connecting to database at: {db_path}")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print all table names and their data
if not tables:
    print("No tables found in the database.")
else:
    for table_name in tables:
        table_name = table_name[0]  # Extract table name from tuple
        print(f"Table: {table_name}")
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print("-" * 40)

# Close the connection
conn.close()
