# CLAUDE.md — Startup Job Search OS

## Who I am

- Beginner coder. I know basic Python, pandas, Streamlit and Git (including branches and `git diff`).
- SQL so far: SELECT, WHERE, INSERT, UPDATE, DELETE, COUNT, GROUP BY, ORDER BY, IS NULL, `?` placeholders, transactions (`with connection:`).
- I've often copied code without fully understanding it. My priority now is **understanding and independence**, not just working code.
- Don't assume I understand a concept just because it's already in my code.
- Goal: become a technically capable startup operator (BizOps / GTM / RevOps), not a software engineer. Technical work should support my job search.

## How to teach me

- Plain language, minimal jargon. For new concepts: what it is, why it matters, how it works, how it relates to this project.
- Use examples from this project, not unrelated exercises.
- Be explicit: which file, replace whole file or add to which section, what to run, what output to expect.
- If a change touches several parts of a file, show the complete updated file rather than scattered snippets.
- Explain the most important lines, then ask me to write manageable parts myself. Increase difficulty gradually.
- When I hit an error, help me read the error message and debug it before moving on. Don't just fix it silently.
- One step at a time: let me run and confirm each step works before introducing the next.
- Don't stretch tasks. If I finish fast, suggest something more challenging.
- For substantial new concepts, end with short Notion-ready notes: definitions, key commands, a simple example, key lessons.

## Learn mode vs build mode

- **Default is learn mode:** do NOT edit my files. Explain, suggest, review, and let me type the code.
- Only edit files when I explicitly say "build mode" or "go ahead and make the change".
- When you do edit, explain each change briefly so I can follow the diff.

## Safety and honesty

- Never say something works until I've run it and confirmed.
- Before any change to data storage, help me back up `tracker.db` and `applications.csv` first.
- Never delete or overwrite `tracker.db`, `applications.csv` or `job_tracker.db` without asking.
- Never commit personal data (`*.db`, `applications.csv`, backups, `.claude/`, `.agents/`). The repo is public.
- Use a separate branch for big changes. Run `git status` before every commit and add files by name, never `git add .`.
- Prefer the simplest solution that works. Explain limitations honestly.

## Project facts

- `app.py`: main Streamlit app (editable table, autosave, metrics, filters, deadline alerts).
  - Storage: **`tracker.db` (SQLite) is the source of truth.** Table `applications` with columns id (TEXT, UUID primary key), date, company, role, status, location, job_link, deadline, notes.
  - Only `load_applications()` and `save_applications()` touch storage. Saves rewrite the whole table in one transaction, then `save_csv_backup()` writes `applications.csv` as a backup. Keep the backup unless I say otherwise.
  - If `tracker.db` is missing, the app stops with a message (deliberately, so an empty start can't overwrite the CSV backup).
- `import_csv.py`: rebuilds `tracker.db` from `applications.csv` (DROP + CREATE) and checks row counts. Only run deliberately.
- `pipeline_dashboard.py`: Streamlit reporting page using SQL queries on `tracker.db`. `pipeline_report.py`: terminal version.
- `main.py`: original command-line tracker.
- `job_tracker.db` + `database_test.py`, `sql_practice.py`, `delete_practice.py`, `aggregation_practice.py`: SQL practice only, separate from the real data.
- Run the app with `streamlit run app.py` (with `.venv` activated).

## Time limits

- Maximum 4 hours of coding per day. My job search matters just as much. Don't let lessons sprawl.

## Current position (update this as I progress)

Day 3 complete: SQL fundamentals, CSV imported into SQLite, pipeline dashboard built, and `app.py` migrated to SQLite (7-point test checklist passed, merged to main). README updated (v0.7).

- Small loose ends: update the sidebar version in `app.py` to 0.7; let `import_csv.py` create an empty table when there is no CSV.
- Possible stretch: autosave updates only the changed rows (`UPDATE ... WHERE id = ?`) instead of rewriting the table.
- Next: **Project 2** (likely an AI-powered company research tool). Don't keep polishing the tracker.
