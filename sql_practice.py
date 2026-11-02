import sqlite3

# The ID of the application you want to update.
# Change this to an ID you can see in the "BEFORE" list.
APPLICATION_ID = 4
NEW_STATUS = "Applied"

# 1. Connect to the database file
connection = sqlite3.connect("job_tracker.db")
cursor = connection.cursor()

# 2. Show every record before the change
print("BEFORE:")
cursor.execute("SELECT id, company, role, status FROM applications")
for row in cursor.fetchall():
    print(row)

# 3. Update one application, identified by its ID
cursor.execute(
    "UPDATE applications SET status = ? WHERE id = ?",
    (NEW_STATUS, APPLICATION_ID),
)
connection.commit()
print(f"\nRows updated: {cursor.rowcount}")

# 4. Fetch that one record again to check the change stuck
cursor.execute(
    "SELECT id, company, role, status FROM applications WHERE id = ?",
    (APPLICATION_ID,),
)
print("AFTER:", cursor.fetchone())

# 5. Close the connection
connection.close()