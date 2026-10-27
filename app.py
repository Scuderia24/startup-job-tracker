
import streamlit as st
import pandas as pd

st.title("Startup Job Search OS")

st.write(
    "Track applications, interviews and startup opportunities in one place."
)

st.subheader("Startup Application Pipeline")

applications = pd.read_csv("applications.csv")

# Calculate application metrics

total = len(applications)

applied = len(
    applications[applications["status"] == "Applied"]
)

interviews = len(
    applications[applications["status"] == "Interview"]
)

interested = len(
    applications[applications["status"] == "Interested"]
)

rejected = len(
    applications[applications["status"] == "Rejected"]
)

offer = len(
    applications[applications["status"] == "Offer"]
)

# Display metrics in six columns

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total", total)
col2.metric("Applied", applied)
col3.metric("Interviews", interviews)
col4.metric("Interested", interested)
col5.metric("Rejected", rejected)
col6.metric("Offer", offer)

st.dataframe(applications, use_container_width=True)

st.write("Total applications:", len(applications))


# Add a new job application

st.subheader("Add New Application")

with st.form("application_form"):

    company = st.text_input("Company")
    role = st.text_input("Job Role")

    status = st.selectbox(
        "Application Status",
        ["Interested", "Applied", "Interview", "Rejected", "Offer"]
    )

    submitted = st.form_submit_button("Add Application")

    if submitted:
        if company.strip() and role.strip():

            new_application = pd.DataFrame([{
                "company": company.strip(),
                "role": role.strip(),
                "status": status
            }])

            updated = pd.concat(
                [applications, new_application],
                ignore_index=True
            )

            updated.to_csv("applications.csv", index=False)

            st.success("Application added successfully!")
            st.rerun()

        else:
            st.error("Please enter both a company and a job role.")
