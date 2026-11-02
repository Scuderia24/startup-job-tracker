
import sqlite3

# Connect to a SQLite database
connection = sqlite3.connect("job_tracker.db")

# Create a cursor to execute SQL
cursor = connection.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        company TEXT,
        role TEXT,
        status TEXT
    )
""")

# Save changes
connection.commit()

# Close connection
connection.close()

print("Database created successfully!")
