from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

DATABASE_FILE = Path(__file__).parent / "tracker.db"

st.set_page_config(page_title="Pipeline Report", layout="wide")
st.title("📊 Pipeline Report")
st.caption("Read-only view of tracker.db. Run import_csv.py to refresh it from your CSV.")

# Stop early with a clear message if the database hasn't been created yet
if not DATABASE_FILE.exists():
    st.error("tracker.db not found. Run `python import_csv.py` first.")
    st.stop()


def run_query(sql, params=()):
    """Run a SQL query against tracker.db and return the result as a DataFrame."""
    connection = sqlite3.connect(DATABASE_FILE)
    df = pd.read_sql_query(sql, connection, params=params)
    connection.close()
    return df


# ---------- Headline metrics ----------
total = run_query("SELECT COUNT(*) AS total FROM applications")["total"][0]

responses = run_query(
    "SELECT COUNT(*) AS responses FROM applications "
    "WHERE status NOT IN ('Applied', 'Ghosted')"
)["responses"][0]

response_rate = responses / total if total > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total applications", total)
col2.metric("Got a response", responses)
col3.metric("Response rate", f"{response_rate:.0%}")

# ---------- Applications by status ----------
st.subheader("Applications by status")
by_status = run_query(
    "SELECT status, COUNT(*) AS applications "
    "FROM applications GROUP BY status ORDER BY applications DESC"
)
st.bar_chart(by_status, x="status", y="applications")

# ---------- YOUR TURN ----------
# Add a section called "Applications with no deadline" that shows
# a table of company and role for every application with no deadline.

st.subheader("Applications with no deadline")
no_deadline = run_query(
    "SELECT company, role FROM applications "
    "WHERE deadline IS NULL ORDER BY company"
)
st.dataframe(no_deadline, hide_index=True)