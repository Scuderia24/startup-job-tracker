import sqlite3

connection = sqlite3.connect("job_tracker.db")
cursor = connection.cursor()

# 1. COUNT: how many applications in total?
cursor.execute("SELECT COUNT(*) FROM applications")
total = cursor.fetchone()[0]
print(f"Total applications: {total}")

# 2. GROUP BY: how many applications at each status?
print("\nApplications by status:")
cursor.execute(
    "SELECT status, COUNT(*) FROM applications GROUP BY status"
)
for status, count in cursor.fetchall():
    print(f"  {status}: {count}")

# 3. COUNT + WHERE: how many applications at the Interview stage?
cursor.execute(
    "SELECT COUNT(*) FROM applications WHERE status = ?",
    ("Interview",)
)
interview_count = cursor.fetchone()[0]
print(f"\nApplications at Interview stage: {interview_count}")

# 4. GROUP BY company: how many applications per company?
print("\nApplications by company:")
cursor.execute(
    "SELECT company, COUNT(*) FROM applications GROUP BY company"
)
for company, count in cursor.fetchall():
    print(f"  {company}: {count}")

connection.close()