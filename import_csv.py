import csv
import sqlite3

CSV_FILE = "applications.csv"
DATABASE_FILE = "tracker.db"

connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

# 1. Start fresh: remove the old table (if any) and create it again.
#    The CSV is still the "real" data, so the database is just a copy
#    we can rebuild at any time by re-running this script.
cursor.execute("DROP TABLE IF EXISTS applications")
cursor.execute("""
    CREATE TABLE applications (
        id TEXT PRIMARY KEY,
        date TEXT,
        company TEXT,
        role TEXT,
        status TEXT,
        location TEXT,
        job_link TEXT,
        deadline TEXT,
        notes TEXT
    )
""")

# 2. Read the CSV (read-only: this script never changes applications.csv)
with open(CSV_FILE, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows_imported = 0

    for row in reader:
        # Empty cells in a CSV come through as "" (empty text).
        # In a database, "no value" should be NULL, which Python calls None.
        clean = {}
        for column, value in row.items():
            if value.strip() == "":
                clean[column] = None
            else:
                clean[column] = value

        cursor.execute(
            """
            INSERT INTO applications
                (id, date, company, role, status, location, job_link, deadline, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                clean["id"],
                clean["date"],
                clean["company"],
                clean["role"],
                clean["status"],
                clean["location"],
                clean["job_link"],
                clean["deadline"],
                clean["notes"],
            ),
        )
        rows_imported += 1

connection.commit()

# 3. Check: does the database have the same number of rows as the CSV?
cursor.execute("SELECT COUNT(*) FROM applications")
rows_in_database = cursor.fetchone()[0]

print(f"Rows read from CSV:   {rows_imported}")
print(f"Rows in the database: {rows_in_database}")

if rows_imported == rows_in_database:
    print("Import check passed.")
else:
    print("WARNING: row counts don't match.")

connection.close()