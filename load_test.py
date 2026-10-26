import csv

applications = []

with open("applications.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        applications.append(row)

    for application in applications:
        print(
            application["company"],
            "|",
            application["role"],
            "|",
            application["status"]
    )

print("Total applications:", len(applications))
