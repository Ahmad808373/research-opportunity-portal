# Assignment verification checklist

Source: all six pages of CN_Assignment1.pdf, sections 1-9, plus the user's detailed
instructions. Status meanings: **Verified** = executed or directly confirmed;
**Implemented but not tested** = prepared but not executed in the target environment;
**Pending** = requires a missing item/action; **Failed** = attempted and unsuccessful.

## Backend and database

| Requirement | Status | Evidence |
|---|---|---|
| Three logical layers: frontend, REST API, MySQL | Verified | Live browser/HTTP tests using real MySQL |
| Auto-generated unique ID | Verified | Three creates returned distinct generated IDs |
| Research title | Verified | schema.sql; required-field and CRUD tests |
| Research description | Verified | schema.sql; required-field and CRUD tests |
| Research area | Verified | schema.sql; required-field and CRUD tests |
| Faculty member name | Verified | schema.sql; required-field and CRUD tests |
| Department | Verified | schema.sql; required-field and CRUD tests |
| Required skills | Verified | schema.sql; required-field and CRUD tests |
| Available positions | Verified | Non-negative INT constraint; invalid-input/direct-SQL tests |
| Application deadline | Verified | DATE; ISO/impossible-date/leap-day tests |
| Open/Closed status | Verified | ENUM/CHECK; validation and close tests |
| Simple one-table schema and setup SQL | Verified | Real MySQL initialized with schema.sql |
| POST /api/opportunities | Verified | 201 create; persisted row |
| GET /api/opportunities | Verified | 200 real rows; [] for empty table |
| GET /api/opportunities/:id | Verified | Complete 200 record; missing/deleted 404 |
| PUT /api/opportunities/:id | Verified | All fields updated; partial close; 400 invalid; 404 missing |
| DELETE /api/opportunities/:id | Verified | 200 delete; absent row; subsequent GET/DELETE 404 |
| HTTP 200, 201, 400, 404, 500 | Verified | Executed API suite/collection; real failed connection produces 500 |
| Required-field validation, safe IDs, invalid JSON | Verified | Live HTTP invalid-input tests |
| Parameterized queries and database safeguards | Verified | SQL-like text retained as data; direct constraints rejected invalid writes |
| No private details in API errors | Verified | Actual 500 JSON inspected by executed test |
| CRUD backed by MySQL; no database substitution | Verified | Real MySQL 8.0.46 used for all CRUD tests |
| Persistence after Flask restart | Verified | Created row retrieved after process restart |
| Persistence after MySQL restart | Verified | database-persistence.json; real stop/start |

## Frontend: all eight PDF functions

| Requirement | Status | Evidence |
|---|---|---|
| 1. Display all opportunities | Verified | Browser list from GET and empty state |
| 2. Display complete selected details | Verified | Single-record GET; every required field rendered |
| 3. Create opportunity | Verified | Browser POST -> MySQL -> refreshed card/details |
| 4. Update opportunity | Verified | Edit form -> PUT -> saved title/positions |
| 5. Open to Closed | Verified | Close button -> PUT -> Closed after reload |
| 6. Delete opportunity | Verified | Confirmation, DELETE, refreshed empty list |
| 7. Success and error messages | Verified | Success, stopped backend, failed-save form message |
| 8. Required-field validation | Verified | Empty/whitespace field; positions/date checks |
| API communication; no hard-coded opportunities | Verified | Real browser requests and SQL-backed records; source review |
| Clear, simple responsive UI | Verified | Inspected 1366px/390px screenshots; no overflow |
| Repeated submit protection | Verified | Two immediate form submits produced one POST |
| Backend unavailability handled | Verified | Actual backend stopped after page load; Refresh/save error displayed |
| Windows 11 local setup and UI smoke test | Implemented but not tested | README ready; application execution environment was Linux |

## GitHub

| Requirement | Status | Evidence |
|---|---|---|
| Repository exists and is public/readable | Verified | Actual metadata and unauthenticated git fetch |
| Actual branch/file/commit write access | Verified | development branch; af9b1bb write-check commit read back |
| Database/backend/frontend/API/testing milestones | Verified | Each remote head confirmed on main and development |
| Backend, frontend, schema, Postman files online | Verified | Published source trees and verified remote commits |
| Complete README/documentation online | Verified | Documentation commit 79cca366 published; README and required paths read back |
| No credentials exposed | Verified | Tracked source review; placeholder .env.example; ignored .env/.venv |
| Actual repository URL in README/submission | Verified | README and GITHUB_LINK.txt contain existing repository URL |
| Instructor access at submission time | Pending | Public now; confirm still accessible when submitting |

Initial 403 write attempts failed, then were resolved by the user's permission
change. They are not counted as successful pushes. Milestones were preserved
locally and then published separately in order. See GITHUB.md and GITHUB_COMMITS.json.

## Postman: all eight mandatory scenarios

| PDF scenario | Status | Evidence |
|---|---|---|
| 1. Create at least three different opportunities | Verified | Collection 01-03, actual 201 responses |
| 2. Retrieve all | Verified | 04, actual array includes three IDs |
| 3. Retrieve one | Verified | 05, complete response with matching ID |
| 4. Update | Verified | 06, saved changed fields |
| 5. Close | Verified | 07, Closed response |
| 6. Delete | Verified | 08, successful ID response |
| 7. Retrieve deleted ID, show 404 | Verified | 09, actual 404 body |
| 8. Invalid/missing data | Verified | 10, actual 400 validation body |
| Collection exported with methods/URLs/headers/bodies/expected responses/tests/variables | Verified | Valid JSON file; all 14 scripts executed |
| Collection execution | Verified | Newman: 14 requests, 42 assertions, zero failures |
| Local Postman desktop visual demonstration | Pending | Same collection ready to import; desktop GUI was not executed here |

## Video

| Requirement | Status | Evidence |
|---|---|---|
| Recording sequence covers running backend/frontend, create/read/update/close/delete, error, API requests/responses | Implemented but not tested | DEMO_PLAN.md, rehearsable 58-second plan |
| Actual demonstration video or valid video link | Pending | No recording provided or fabricated |
| Actual duration <=60 seconds | Pending | Verify exported recording duration |

## Submission and original PDF instructions

| Requirement | Status | Evidence |
|---|---|---|
| Complete frontend/backend source and schema | Verified | Working source; executed tests |
| Exported collection and README setup/run instructions | Verified | Prepared real files; API collection executed |
| Actual repository link included | Verified | GITHUB_LINK.txt and README |
| Video/video link included | Pending | Await actual recording/link |
| Exact P24 0000 NAME CLASS.zip filename | Pending | Need exact registration number, submission name, and class |
| Final single submission ZIP | Pending | Working package only until video/naming/local demonstration complete |
| No .env, virtual environments, tokens, unnecessary temporary files in working package | Verified | Actual archive inspected; final named submission still pending |
| Both frontend/backend and database CRUD | Verified | Full end-to-end executions |
| Run using README on another Windows computer | Implemented but not tested | Exact-file Windows instructions; local install pending |
| Individual assignment and originality | Pending | Student must understand/adapt the work and follow university assistance policy |

Do not label the assignment submission complete while pending items remain.
TEST_REPORT.md and test-evidence contain the executed results; README and
LEARNING_GUIDE.md explain the implementation in simple language.
