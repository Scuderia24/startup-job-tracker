
from pathlib import Path
from datetime import date
from uuid import uuid4
import os
import tempfile

import pandas as pd
import streamlit as st


# ==========================================
# 1. CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Startup Job Search OS",
    page_icon="🚀",
    layout="wide"
)

CSV_FILE = Path(__file__).parent / "applications.csv"

STATUSES = [
    "Applied",
    "Online Assessment",
    "Video Interview",
    "Interview",
    "Assessment Centre",
    "Offer",
    "Rejected",
    "Withdrawn",
    "Ghosted"
]

STATUS_ICONS = {
    "Applied": "🔵",
    "Online Assessment": "🟣",
    "Video Interview": "🟡",
    "Interview": "🟠",
    "Assessment Centre": "🟤",
    "Offer": "🟢",
    "Rejected": "🔴",
    "Withdrawn": "⚫",
    "Ghosted": "⚫"
}

STATUS_LABELS = {
    status: f"{STATUS_ICONS[status]} {status}"
    for status in STATUSES
}

REVERSE_STATUSES = {
    label: status
    for status, label in STATUS_LABELS.items()
}

COLUMNS = [
    "id",
    "date",
    "company",
    "role",
    "status",
    "location",
    "job_link",
    "deadline",
    "notes"
]

TEXT_COLUMNS = [
    "company",
    "role",
    "status",
    "location",
    "job_link",
    "notes"
]

DATE_COLUMNS = ["date", "deadline"]

TODAY = date.today()


# ==========================================
# 2. SAVE DATA
# ==========================================

def save_applications(df):

    saved = df.reindex(columns=COLUMNS).copy()

    for column in DATE_COLUMNS:
        saved[column] = pd.to_datetime(
            saved[column],
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".csv",
            dir=CSV_FILE.parent,
            delete=False,
            newline="",
            encoding="utf-8"
        ) as temp:

            temp_path = temp.name
            saved.to_csv(temp, index=False)

        os.replace(temp_path, CSV_FILE)

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ==========================================
# 3. LOAD DATA
# ==========================================

def load_applications():

    if CSV_FILE.exists():
        df = pd.read_csv(
            CSV_FILE,
            dtype="string"
        )
    else:
        df = pd.DataFrame(columns=COLUMNS)

    changed = False

    for column in COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA
            changed = True

    df = df[COLUMNS].copy()

    for i in df.index:

        record_id = df.at[i, "id"]

        if pd.isna(record_id) or not str(record_id).strip():
            df.at[i, "id"] = str(uuid4())
            changed = True

    for column in TEXT_COLUMNS:
        df[column] = df[column].astype("string")

    # Migrate old Interested records
    interested_mask = df["status"] == "Interested"

    if interested_mask.fillna(False).any():
        df.loc[interested_mask.fillna(False), "status"] = "Applied"
        changed = True

    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        ).dt.date

    df = df.reset_index(drop=True)

    if changed:
        save_applications(df)

    return df


applications = load_applications()


# ==========================================
# 4. DEADLINE CALCULATIONS
# ==========================================

def add_deadline_calculations(df):

    result = df.copy()

    deadlines = pd.to_datetime(
        result["deadline"],
        errors="coerce"
    )

    result["days_until_deadline"] = (
        deadlines - pd.Timestamp(TODAY)
    ).dt.days.astype("Int64")

    result["deadline_alert"] = ""

    urgent = result[
        "days_until_deadline"
    ].between(0, 3).fillna(False)

    result.loc[urgent, "deadline_alert"] = "🟡 Due soon"

    overdue = (
        result["days_until_deadline"] < 0
    ).fillna(False)

    result.loc[overdue, "deadline_alert"] = "🔴 Overdue"

    return result


# ==========================================
# 5. AUTOSAVE
# ==========================================

def autosave(editor_key, visible_ids):

    changes = st.session_state[editor_key]

    updated = load_applications()

    # Update existing records by stable ID
    for row_index, edits in changes.get(
        "edited_rows", {}
    ).items():

        row_index = int(row_index)

        if row_index >= len(visible_ids):
            continue

        record_id = visible_ids[row_index]

        matches = updated.index[
            updated["id"] == record_id
        ]

        if len(matches) == 0:
            continue

        actual_index = matches[0]

        for column, value in edits.items():

            if column not in COLUMNS or column == "id":
                continue

            if column == "status":
                value = REVERSE_STATUSES.get(
                    value,
                    value
                )

            updated.at[actual_index, column] = value

    # Delete selected records
    deleted_ids = []

    for row_index in changes.get(
        "deleted_rows", []
    ):
        if row_index < len(visible_ids):
            deleted_ids.append(visible_ids[row_index])

    if deleted_ids:
        updated = updated[
            ~updated["id"].isin(deleted_ids)
        ].copy()

    # Add new records
    for row in changes.get("added_rows", []):

        company = str(
            row.get("company") or ""
        ).strip()

        role = str(
            row.get("role") or ""
        ).strip()

        if not company or not role:
            continue

        new_row = {
            column: None
            for column in COLUMNS
        }

        new_row.update({
            key: value
            for key, value in row.items()
            if key in COLUMNS and key != "id"
        })

        new_row["id"] = str(uuid4())

        # Always default to today if blank
        if pd.isna(new_row["date"]) or new_row["date"] == "":
            new_row["date"] = TODAY

        status = new_row["status"]

        if status in REVERSE_STATUSES:
            status = REVERSE_STATUSES[status]

        if not status or status == "Interested":
            status = "Applied"

        new_row["status"] = status

        updated = pd.concat(
            [updated, pd.DataFrame([new_row])],
            ignore_index=True
        )

    updated = updated.reset_index(drop=True)

    save_applications(updated)


# ==========================================
# 6. SIDEBAR
# ==========================================

with st.sidebar:

    st.header("🚀 Startup Job Search OS")
    st.caption("Your personal career dashboard")
    st.divider()
    st.caption("Built with Python + Streamlit")
    st.caption("Version 0.6")


# ==========================================
# 7. HEADER
# ==========================================

st.title("🚀 Startup Job Search OS")

st.caption(
    "Track applications, manage your pipeline "
    "and monitor progress."
)

st.divider()


# ==========================================
# 8. APPLICATION OVERVIEW
# ==========================================

st.subheader("Application Overview")

counts = applications["status"].value_counts()

metrics = [
    ("Total", len(applications)),
    ("Applied", counts.get("Applied", 0)),
    ("Online Assessments", counts.get("Online Assessment", 0)),
    ("Video Interviews", counts.get("Video Interview", 0)),
    ("Interviews", counts.get("Interview", 0)),
    ("Rejections", counts.get("Rejected", 0)),
    ("Offers", counts.get("Offer", 0))
]

cols = st.columns(7)

for col, (label, value) in zip(cols, metrics):
    col.metric(label, int(value))


# ==========================================
# 9. PERSISTENT FILTERS VIA URL
# ==========================================

st.divider()
st.subheader("My Job Applications")

params = st.query_params

saved_search = params.get("search", "")
saved_sort = params.get(
    "sort",
    "Date Added (Newest)"
)

SORT_OPTIONS = [
    "Date Added (Newest)",
    "Date Added (Oldest)",
    "Deadline (Soonest)",
    "Company (A-Z)",
    "Status"
]

if saved_sort not in SORT_OPTIONS:
    saved_sort = SORT_OPTIONS[0]

saved_statuses = [
    status
    for status in params.get_all("status")
    if status in STATUSES
]

search_col, filter_col, sort_col = st.columns(
    [3, 2, 2]
)

with search_col:
    search_query = st.text_input(
        "Search",
        value=saved_search,
        placeholder="Search company or job title..."
    )

with filter_col:
    selected_statuses = st.multiselect(
        "Filter by status",
        STATUSES,
        default=saved_statuses
    )

with sort_col:
    sort_option = st.selectbox(
        "Sort by",
        SORT_OPTIONS,
        index=SORT_OPTIONS.index(saved_sort)
    )

# Store preferences in URL
if search_query:
    st.query_params["search"] = search_query
else:
    if "search" in st.query_params:
        del st.query_params["search"]

st.query_params["sort"] = sort_option

if selected_statuses:
    st.query_params["status"] = selected_statuses
else:
    if "status" in st.query_params:
        del st.query_params["status"]


# ==========================================
# 10. FILTER APPLICATIONS
# ==========================================

filtered = applications.copy()

if search_query:

    mask = (
        filtered["company"].str.contains(
            search_query,
            case=False,
            na=False,
            regex=False
        )
        |
        filtered["role"].str.contains(
            search_query,
            case=False,
            na=False,
            regex=False
        )
    )

    filtered = filtered[mask.fillna(False)]

if selected_statuses:
    filtered = filtered[
        filtered["status"].isin(selected_statuses)
    ]


# ==========================================
# 11. SORT APPLICATIONS
# ==========================================

if sort_option == "Date Added (Newest)":

    filtered = filtered.sort_values(
        "date",
        ascending=False,
        na_position="last",
        kind="stable"
    )

elif sort_option == "Date Added (Oldest)":

    filtered = filtered.sort_values(
        "date",
        ascending=True,
        na_position="last",
        kind="stable"
    )

elif sort_option == "Deadline (Soonest)":

    filtered = filtered.sort_values(
        "deadline",
        ascending=True,
        na_position="last",
        kind="stable"
    )

elif sort_option == "Company (A-Z)":

    filtered = filtered.sort_values(
        "company",
        kind="stable"
    )

elif sort_option == "Status":

    filtered = filtered.sort_values(
        "status",
        kind="stable"
    )

filtered = filtered.reset_index(drop=True)


# ==========================================
# 12. PREPARE EDITOR
# ==========================================

editor_data = add_deadline_calculations(filtered)

editor_data["status"] = (
    editor_data["status"].map(STATUS_LABELS)
    .fillna(editor_data["status"])
)

visible_ids = filtered["id"].tolist()

# Editor key changes with filters and sorting
editor_key = (
    "application_editor_"
    + str(hash((
        search_query,
        tuple(selected_statuses),
        sort_option
    ))).replace("-", "n")
)


# ==========================================
# 13. EDITABLE TABLE
# ==========================================

st.data_editor(
    editor_data,
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True,
    height=460,
    column_order=[
        "date",
        "company",
        "role",
        "status",
        "location",
        "job_link",
        "deadline",
        "days_until_deadline",
        "deadline_alert",
        "notes"
    ],
    column_config={

        "id": None,

        "date": st.column_config.DateColumn(
            "Date Added",
            format="DD/MM/YYYY"
        ),

        "company": st.column_config.TextColumn(
            "Company",
            required=True
        ),

        "role": st.column_config.TextColumn(
            "Job Title",
            required=True
        ),

        "status": st.column_config.SelectboxColumn(
            "Status",
            options=list(STATUS_LABELS.values())
        ),

        "location": st.column_config.TextColumn(
            "Location"
        ),

        "job_link": st.column_config.LinkColumn(
            "Job Posting"
        ),

        "deadline": st.column_config.DateColumn(
            "Deadline",
            format="DD/MM/YYYY"
        ),

        "days_until_deadline": (
            st.column_config.NumberColumn(
                "Days Until Deadline",
                format="%d",
                disabled=True
            )
        ),

        "deadline_alert": st.column_config.TextColumn(
            "Deadline Alert",
            disabled=True
        ),

        "notes": st.column_config.TextColumn(
            "Notes",
            width="large"
        )
    },
    key=editor_key,
    on_change=autosave,
    args=(editor_key, visible_ids)
)

st.caption(
    f"Showing {len(filtered)} of "
    f"{len(applications)} applications"
)


# ==========================================
# 14. DEADLINES WITHIN 3 DAYS
# ==========================================

st.divider()

st.subheader("Deadlines within 3 days")

summary = add_deadline_calculations(applications)

upcoming = summary[
    summary["days_until_deadline"]
    .between(0, 3)
    .fillna(False)
].copy()

upcoming = upcoming.sort_values(
    "days_until_deadline"
)

if upcoming.empty:

    st.success(
        "No application deadlines within 3 days."
    )

else:

    st.warning(
        f"{len(upcoming)} application deadline(s) "
        "coming up."
    )

    st.dataframe(
        upcoming[
            [
                "company",
                "status",
                "deadline",
                "days_until_deadline"
            ]
        ],
        hide_index=True,
        use_container_width=True,
        column_config={

            "company": "Company",

            "status": "Status",

            "deadline": st.column_config.DateColumn(
                "Deadline",
                format="DD/MM/YYYY"
            ),

            "days_until_deadline": (
                st.column_config.NumberColumn(
                    "Days Until Deadline",
                    format="%d"
                )
            )
        }
    )
