import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Disable foreign key constraints
cursor.execute("PRAGMA foreign_keys = OFF;")
conn.commit()

# List of tables to delete data from with correct names
tables = [
    'base_heart_disease', 'base_heart_patient', 'base_diabetes',
    'base_diabetes_patient', 'base_parkinsons', 'base_parkinsons_patient', 'base_save_doctor'
]

# Delete data from all listed tables
for table in tables:
    try:
        cursor.execute(f"DELETE FROM {table};")
    except sqlite3.OperationalError as e:
        print(f"Error deleting data from {table}: {e}")

# Re-enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")
conn.commit()

# Close the connection
conn.close()
