
applications = [
    {
        "company": "Monzo",
        "role": "Growth Associate",
        "status": "Interested"
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
    }
]

ramp_application = {
    "company": "Ramp",
    "role": "Strategy & Operations Associate",
    "status": "Interested"
}

applications.append(ramp_application)

anthropic_application = {
    "company": "Anthropic",
    "role": "GTM Associate",
    "status": "Interested"
}

applications.append(anthropic_application)

stripe_application = {
    "company": "Stripe",
    "role": "BizOps Intern",
    "status": "Interested"
}

applications.append(stripe_application)

applications[0]["status"] = "Applied"
applications[3]["status"] = "Applied"
applications[4]["status"] = "Interview"

print("ADD A NEW JOB APPLICATION")

company = input("Enter company name: ")
role = input("Enter job role: ")
status = input("Enter application status: ")

print("----------------------")
print("Company:", company)
print("Role:", role)
print("Status:", status)

new_application = {
    "company": company,
    "role": role,
    "status": status
}

print("New application:")
print(new_application)

applications.append(new_application)

print("Application added!")
print("Total applications:", len(applications))

# Job Search Analysis 

total_applications = len(applications)

applied_count = 0
interview_count = 0
interested_count = 0 

print("-----------------------")
print("MY STARTUP APPLICATIONS")
print("-----------------------")

for application in applications:
    print(
        application["company"],
        "|",
        application["role"],
        "|",
        application["status"]
    )

for application in applications:

    if application["status"] == "Applied":
        applied_count += 1

    if application["status"] == "Interview":
        interview_count += 1

    if application["status"] == "Interested":
        interested_count += 1

print("-------------------------")
print("JOB SEARCH ANALYTICS")
print("-------------------------")

print("Total applications:", total_applications)
print("Applied:", applied_count)
print("Interviews:", interview_count)
print("Interested:", interested_count)
