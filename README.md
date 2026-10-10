# University Research Opportunity Portal

Computer Networks Assignment 01: a small faculty research-opening management app.
HTML/CSS/vanilla JavaScript calls a Python Flask REST API, and every opportunity is
stored in MySQL. There is no login, student application system, or analytics.

GitHub: https://github.com/Ahmad808373/research-opportunity-portal

**Publishing status:** GitHub write access was verified after the connection
permissions were corrected. Database, backend, frontend, and API integration
milestones have been published and verified. Testing/documentation publication
and the final file check are in progress; see docs/VERIFICATION.md.

## Features and technologies

- Display all opportunities and a selected opportunity's complete details.
- Create, edit, close, and delete database records; confirm before deleting.
- Validate fields and show success, validation, server, and connection messages.
- Prevent repeated form submissions while a request is running.
- Responsive layout; no hard-coded opportunities.

Python 3.12, Flask 3.1.2, mysql-connector-python 9.4.0, python-dotenv 1.1.1,
MySQL 8.0.16+, HTML5, CSS3, JavaScript, Postman, and Git/GitHub.
Only three direct Python dependencies are needed. Node/Newman/Playwright are
optional test tools, not application requirements.

## Project structure

| Location | Purpose |
|---|---|
| `backend/app.py` | Five REST endpoints, validation, HTTP responses; serves frontend |
| `backend/db.py` | Read configuration; open/close MySQL connections |
| `backend/requirements.txt` | Python dependencies |
| `backend/.env.example` | Local configuration template with placeholders |
| `frontend/index.html` | List, full details, create/edit form |
| `frontend/style.css` | Responsive appearance |
| `frontend/script.js` | Fetch calls, rendering, frontend validation |
| `database/schema.sql` | Database, table, constraints |
| `postman/Research_Opportunity_Portal.postman_collection.json` | Ordered requests and assertions |
| `tests/test_api.py` | Optional live HTTP/MySQL regression suite |
| `tests/test_frontend.cjs` | Optional browser regression suite |
| `docs/REQUIREMENTS.md` | Complete original PDF checklist |
| `docs/VERIFICATION.md` | Evidence-based final requirement statuses |
| `docs/LEARNING_GUIDE.md` | Explanation and instructor questions |
| `docs/DEMO_PLAN.md` | Recording preparation and 58-second sequence |
| `docs/GITHUB.md` | Publication steps and permission limitation |
| `docs/TEST_REPORT.md` | Actual results and local verification procedure |
| `docs/SUBMISSION.md` | Pending items and final ZIP instructions |

## Windows 11 setup

Install Python 3.12 with the Python launcher, MySQL Server 8.0.16+ and MySQL
Workbench, VS Code, Postman desktop, and Git for Windows. Start the MySQL service.
Keep your MySQL administrator password local.

Extract the package. Open the `research-opportunity-portal` folder in VS Code.
Open **Terminal > New Terminal**, select **PowerShell**, and work from the project
root (where this README is).

### 1. Virtual environment and dependencies

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Using the environment's Python directly avoids activation-policy errors. Optional
activation is `.\.venv\Scripts\Activate.ps1`; it is unnecessary for commands below.
Select `.venv` as your VS Code Python interpreter if prompted.

### 2. MySQL database

In Workbench, connect as your local administrator. Choose **File > Open SQL Script**,
select `database/schema.sql`, and execute the entire script. Refresh Schemas.
You should see database `research_portal`, table `opportunities`.
The script is safe to rerun and does not delete existing records.

Alternatively, inside the MySQL command-line client:

```sql
SOURCE C:/YOUR_PATH/research-opportunity-portal/database/schema.sql;
```

Replace YOUR_PATH with your actual folder; use forward slashes in SOURCE.

As administrator, execute the following in Workbench, replacing the password
placeholder **only in Workbench**, not in committed files:

```sql
CREATE USER IF NOT EXISTS 'portal_user'@'localhost'
    IDENTIFIED BY 'YOUR_LOCAL_PASSWORD';
GRANT SELECT, INSERT, UPDATE, DELETE
    ON research_portal.* TO 'portal_user'@'localhost';
```

If this account already exists, CREATE USER IF NOT EXISTS does not change its
password. Use its existing password or change it locally with ALTER USER.
The application account needs only these four data permissions.

### 3. Local configuration

```powershell
Copy-Item backend\.env.example backend\.env
```

Open `backend/.env`. Replace DB_PASSWORD with your local portal_user password.
Keep DB_NAME=research_portal and set DB_PORT to MySQL's actual port (normally 3306).
Do not put a real password in `.env.example`. The real `.env` is ignored by Git.

### 4. Run the application

```powershell
.\.venv\Scripts\python.exe backend\app.py
```

Leave that terminal running and open **http://127.0.0.1:5000/** in your browser.
Flask serves the frontend and API at the same address. Do not double-click
index.html or use VS Code Live Server: fetch uses same-origin /api/opportunities.
Flask-CORS and a second frontend server are unnecessary.

Stop with Ctrl+C; restart with the same command. Records remain in MySQL.
If port 5000 is occupied, change PORT in `.env` and use that port in both your
browser and the Postman base_url variable.

## Using the interface

Click **Add Opportunity**, fill every field, and **Save Opportunity**. The list
refreshes from the API and shows the stored record. **View details** retrieves the
full record. **Edit Opportunity** opens existing values. **Close Opportunity**
sends a status-only PUT and displays Closed. The edit form can also reopen a record.
**Delete Opportunity** asks for confirmation, deletes it, and refreshes the list.
**Refresh** retrieves the current database records.

Zero positions is valid; negative positions are invalid. Past deadlines are allowed
because the assignment requires a valid date, not a future date. Closing is explicit;
the application does not automatically close records. Required text is trimmed;
spaces alone are rejected. Status must be exactly Open or Closed.

## API endpoints

Use Content-Type: application/json for request bodies. URLs are relative to
http://127.0.0.1:5000. Replace ID with an actual ID returned by POST.

| Method | Endpoint | Successful response |
|---|---|---|
| POST | `/api/opportunities` | 201, `{message, opportunity}` |
| GET | `/api/opportunities` | 200, array of records or `[]` |
| GET | `/api/opportunities/ID` | 200, complete record object |
| PUT | `/api/opportunities/ID` | 200, `{message, opportunity}` |
| DELETE | `/api/opportunities/ID` | 200, `{message, id}` |

Example POST input (not built-in application data):

```json
{
  "title": "Network Traffic Analysis",
  "description": "Analyze congestion in the university network.",
  "research_area": "Computer Networks",
  "faculty_name": "Dr. Example Faculty",
  "department": "Computer Science",
  "required_skills": "Python, TCP/IP, Wireshark",
  "available_positions": 2,
  "application_deadline": "2026-12-20",
  "status": "Open"
}
```

POST requires all nine non-ID fields. MySQL generates id. PUT accepts one or more
editable fields, merges them with the stored record, then validates the result.
Empty bodies and unknown fields are rejected; id cannot be edited.
To close, send `{"status":"Closed"}` in a PUT.

Errors use `{"error":"Meaningful message"}`:

| Code | Meaning |
|---|---|
| 200 | Retrieval, update, or deletion succeeded |
| 201 | New record stored |
| 400 | Invalid/missing field, malformed JSON, or invalid ID |
| 404 | Valid ID does not exist, or route not found |
| 500 | Database unavailable or unexpected server error |

Dates are real YYYY-MM-DD dates, years 1000-9999. Positions must be a JSON integer
from 0 to 2147483647, not a string/decimal/boolean. IDs are positive integers in that
range. Text limits are in TEXT_LIMITS. Queries use parameters, not interpolated user
values. Connections close after each request; unfinished transactions roll back.
Each mutation commits after success. API responses do not expose SQL error text,
credentials, or stack traces. Flask debug mode is disabled.

## Postman import and required demonstration

1. Start MySQL and Flask; open Postman desktop.
2. Choose **Import > Files** and select the JSON in `postman/`.
3. In collection Variables, set base_url to your Flask address without a trailing
   slash. No environment is required. The create requests fill ID variables.
4. Run requests **01-14 in order**, one iteration, using Collection Runner.
5. Inspect Tests/Results and each request's response status and body.

01-03 create three different opportunities; 04 retrieves all; 05 retrieves one;
06 updates; 07 closes; 08 deletes; 09 requests the deleted ID and expects 404;
10 sends missing data and expects 400. These cover all eight PDF scenarios.
11-14 also check negative positions, invalid date/status, and malformed JSON.

Two records remain for your frontend demo. Reruns create new records and use newly
returned IDs; they do not delete your other records. Delete demonstration records
in the UI afterward if desired. Do not send request 05 before request 01 fills its ID.

Optional 500 check: stop MySQL, resend GET all, inspect the safe 500 response,
then restart MySQL. The one-minute video needs at least one 400 or 404, not every
supporting error case.

## Testing and running on another computer

Executed here: 13 live HTTP/MySQL test groups; 14 Postman collection requests with
42 passing assertions via Newman; 16 browser checks; actual MySQL restart persistence.
See [test report](docs/TEST_REPORT.md). Postman desktop GUI and Windows installation
were not executed here; complete them locally. Application tests ran on Linux.

Optional Python suite: it clears its target table and refuses DB_NAME values that
 do not end in `_test`. Never target your main database. In a separate Workbench
query tab, create research_portal_test by copying schema.sql and changing both
research_portal occurrences to research_portal_test. Grant your local app user
SELECT, INSERT, UPDATE, DELETE on research_portal_test.* as well. In a separate
PowerShell terminal at project root:

```powershell
$env:DB_NAME="research_portal_test"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
Remove-Item Env:DB_NAME
```

Other credentials are loaded from backend/.env. The suite starts its own Flask
server on port 5010, so keep that port free. It tests full CRUD, validation,
constraints, nonexistent IDs, failed/unchanged updates, SQL-like text, server
restart persistence, and real connection failure.

Optional browser suite requires Node and `npm install --no-save playwright`, then
`npx playwright install chromium`. Start Flask against an EMPTY disposable test
database and run `node tests/test_frontend.cjs`. Do not set PORTAL_SERVER_PID locally;
that option belongs to the advanced process-stopping test harness. Your required
assignment demonstration remains Postman.

On another computer, copy/download the source and repeat setup steps 1-4. Create
that computer's own dependencies, MySQL database, local user, and .env. Passwords
and live database records are not packaged. MySQL stores data separately from Flask.

## Troubleshooting

| Problem | Solution |
|---|---|
| py not recognized | Install Python with its launcher; reopen VS Code |
| No module named flask | Install and run using the same .venv Python |
| Activate.ps1 blocked | Use the direct environment Python commands above |
| Database operation failed | Start MySQL; check .env credentials/port, database and table |
| MySQL Access denied | Check local user, password, host, and database grants |
| Unknown database/table | Execute the whole schema.sql in Workbench |
| Port occupied | Change PORT and browser/Postman URLs |
| Frontend file opens but API fails | Open the Flask URL, not index.html or Live Server |
| Invalid JSON | In Postman choose Body > raw > JSON and correct quotes/commas |
| Record returns 404 | Use a saved ID; deleted records remain deleted |
| Cannot reach backend | Restart Flask, then Refresh; failed-save form values remain |
| UI cannot open at all | Flask must run to serve the HTML as well |
| Saved but refresh failed | Press Refresh; do not resubmit the saved change |
| .env changes seem ignored | Remove overriding DB_* or PORT environment variables and restart |

Read [the learning guide](docs/LEARNING_GUIDE.md), follow [the recording plan](docs/DEMO_PLAN.md),
and check [submission instructions](docs/SUBMISSION.md). The working package is
**not the final named submission**: source publication, local Postman GUI demonstration,
exact personal filename details, and a real recording remain pending.
