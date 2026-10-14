# Actual test report

Executed on 10 October 2026 in the development environment. These are real
executions, not expected-result examples. Evidence files are in `test-evidence/`.

## Environment and scope

- Ubuntu Linux test environment; Python 3.12; Flask 3.1.2;
  mysql-connector-python 9.4.0; real MySQL 8.0.46 with InnoDB.
- Database: a disposable research_portal_test initialized from schema.sql.
  No SQLite, fake persistence, or mocked CRUD database was used.
- Separate Python HTTP client requests against a real Flask subprocess.
- Newman 6.2.3 executed the actual exported Postman collection and its scripts.
- Playwright controlled a real headless Chromium browser at 1366px and 390px widths.
- Test MySQL ran on port 3307; normal Windows setup defaults to 3306. This difference
  was supplied through environment variables, not a source-code change.

## Results

| Test group | Executed outcome | Evidence |
|---|---|---|
| Python live HTTP/MySQL regression suite | 13 test methods passed; subtests cover many invalid inputs | api-tests.txt |
| Exported Postman collection | 14 requests, 42 assertions, 0 failures | postman-results-summary.json |
| Browser regression suite | 16 named checks passed; no uncaught JavaScript errors | frontend-tests.txt, frontend-results.json |
| Persistence after Flask restart | Created record retrieved unchanged after actual Flask stop/start | test_persistence_after_flask_restart in api-tests.txt |
| Persistence after MySQL restart | Committed row retrieved after actual MySQL stop/start | database-persistence.json |
| Desktop/mobile appearance | Real browser screenshots inspected; final mobile spacing corrected | desktop.png, mobile.png |

The screenshots show example input actually stored by the API in the test database.
They are not a one-minute recording or fabricated application output.

## Functional coverage

The API suite created three distinct rows and verified generated unique IDs, list
and complete single-record retrieval, editing every field, zero positions, unchanged
updates returning 200, Open-to-Closed persistence, deletion, subsequent GET 404,
and repeat DELETE 404. A direct SQL query confirmed the deleted ID was absent.

It tested empty-database `[]`, each required field missing/null/empty/spaces,
negative/decimal/string/boolean/out-of-range positions, impossible/non-ISO dates,
valid leap day, unsupported status, malformed JSON and non-object JSON, wrong
content type, unknown fields, overlong title, invalid IDs and nonexistent IDs for
GET/PUT/DELETE. Invalid updates left the original row unchanged. SQL-like text
was stored as text without altering the table. Direct SQL constraint violations
were rejected by MySQL.

For the 500 check, the test stopped its Flask process and restarted it with a
closed database port, creating a real connection failure. The API returned safe
JSON 500 and did not expose SQL, traceback text, or connection settings.

The browser suite checked empty state, native required validation, negative positions,
an impossible deadline, whitespace-only title, one POST for two immediate submit
events, successful create, GET full details, safe rendering of HTML-like text,
edit with zero positions, close, reload persistence, 390px layout without overflow,
delete cancellation, confirmed deletion, error after an actual stopped backend,
failed-save form retention, and no uncaught JavaScript errors. Some related checks
are grouped under one named check; 16 is the named-check count, not a claim that
only 16 individual assertions were evaluated.

## Defects found and fixed

- A Postman list-check script initially had a parenthesis error. It was corrected;
  every collection script parsed, and the full rerun passed 42 assertions.
- The heading initially joined two words when its desktop line break was hidden
  on mobile. A literal space was added and a browser assertion verifies the final
  heading reads University Research Opportunity Portal at 390px.

The final browser suite was rerun after the heading correction and the additional
deadline check. Already passing API/collection tests were not changed afterward.

## Not executed here

- Windows installation, Workbench UI setup, and VS Code setup on Ahmad's computer.
  The Windows commands were prepared for the actual file structure; app execution
  tests used Linux. Complete the local smoke test below.
- Postman desktop GUI interaction and screen recording. Newman verified the same
  collection file, but it is not a claim that the desktop GUI was demonstrated.
- An actual <=60-second video. Only a recording plan is supplied.
- Every possible browser/version, concurrent multi-user load, or production hosting.
  These are outside this simple local university assignment's scope.

## Exact local verification procedure

1. Follow README Windows steps; open the Flask URL and confirm the empty/list view.
2. In Postman import the collection, set base_url, run 01-14 in order, and inspect
   passing assertions plus the actual 201/200/400/404 response bodies.
3. In the UI add a different record. View it, edit it, close it, reload the page,
   delete it, and confirm its ID returns 404 in Postman.
4. Submit blank fields, a negative position value, and an empty deadline. Check
   meaningful feedback and no invalid row added. Backend invalid-date checks are
   available in collection request 12.
5. Try pressing Save twice quickly; only one record should be created for that save.
6. Create a record, stop/restart Flask, and retrieve it. Then restart MySQL and
   retrieve it again. Do not rerun DROP/TRUNCATE or reset the database during this test.
7. Keep the page open, stop Flask, and click Refresh. Check its connection message;
   restart Flask and Refresh. A brand-new page cannot load while Flask is stopped
   because Flask serves the HTML too.
8. Optionally stop MySQL while Flask stays running: GET all should return JSON 500;
   restart MySQL and confirm normal behavior returns.
9. Record the real workflow and Postman output according to DEMO_PLAN.md.


## Final submission update - 14 October 2026

The student supplied a real Windows screen recording showing the renamed
portal_app.py entry point, frontend CRUD, 42 passed Postman GUI assertions, and
a live 404 JSON response. A 59.80-second reviewed copy is included in the final ZIP.
All API, exported collection, and browser tests were rerun successfully after
the entry-point rename. See docs/submission-tests/RESULTS.md and its transcripts.
The earlier "Not executed here" notes describe the original development run;
they are superseded for the student's Windows/Postman demonstration and video.
Historical screenshots remain in the GitHub repository. The final ZIP contains
text/JSON evidence only and excludes screenshot files.
