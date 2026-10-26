import csv

# Step 1: Load existing applications

applications = []

with open("applications.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        applications.append(row)

print("Welcome to Startup Job Search OS!")
print("-------------------------------")
print("Loaded applications:", len(applications))

# Step 2: Collect a new application

print("\nADD A NEW APPLICATION")

company = input("Company name: ")
role = input("Job role: ")
status = input("Application status: ")

new_application = {
    "company": company,
    "role": role,
    "status": status
}

applications.append(new_application)

# Step 3: Save all applications to CSV

with open("applications.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["company", "role", "status"]
    )

    writer.writeheader()
    writer.writerows(applications)

print("Applications saved successfully!")
print("\nApplication added!")
print("Total applications:", len(applications))