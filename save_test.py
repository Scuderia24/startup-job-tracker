
import csv

applications = [
    {
        "company": "Monzo",
        "role": "Growth Associate",
        "status": "Applied"
    },
    {
        "company": "ElevenLabs",
        "role": "Business Operations Associate",
        "status": "Applied"
    },
    {
        "company": "Linear",
        "role": "GTM Associate",
        "status": "Interview"
    },
    {
        "company": "Ramp",
        "role": "Strategy & Operations Associate",
        "status": "Interested"
    }
]

with open("applications.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["company", "role", "status"]
    )

    writer.writeheader()
    writer.writerows(applications)

print("Applications saved successfully!")
