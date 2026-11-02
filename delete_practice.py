import sqlite3

# Change these to the IDs of your duplicate rows
IDS_TO_DELETE = [1, 2, 4, 5]

connection = sqlite3.connect("job_tracker.db")
cursor = connection.cursor()

print("BEFORE:")
cursor.execute("SELECT id, company, role, status FROM applications")
for row in cursor.fetchall():
    print(row)

for application_id in IDS_TO_DELETE:
    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,)
    )
    
connection.commit()

print("\nAFTER:")
cursor.execute("SELECT id, company, role, status FROM applications")
for row in cursor.fetchall():
    print(row)

connection.close()