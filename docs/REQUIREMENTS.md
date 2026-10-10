# Assignment requirements and implementation decisions

Source: CN_Assignment1.pdf, all six pages, sections 1-9. The PDF is authoritative.
The user's detailed instructions add validation, Windows setup, and testing requirements.

## Exact PDF checklist

- [ ] Section 1: university faculty opportunity management; frontend, REST API, database.
- [ ] Section 2: unique ID, title, description, research area, faculty name, department,
  required skills, available positions, application deadline, Open/Closed status.
- [ ] 2.1: POST /api/opportunities creates a database record.
- [ ] 2.2: GET /api/opportunities retrieves all database records.
- [ ] 2.3: GET /api/opportunities/:id retrieves complete details.
- [ ] 2.4: PUT /api/opportunities/:id updates a record, including status.
- [ ] 2.5: DELETE /api/opportunities/:id deletes a record.
- [ ] 2.6: appropriate HTTP 200, 201, 400, 404, 500.
- [ ] Section 3.1: display all opportunities.
- [ ] Section 3.2: display selected opportunity's complete details.
- [ ] Section 3.3: create form.
- [ ] Section 3.4: update form.
- [ ] Section 3.5: change Open to Closed.
- [ ] Section 3.6: delete.
- [ ] Section 3.7: success and error messages.
- [ ] Section 3.8: required-field validation.
- [ ] Section 3: frontend calls REST API; no hard-coded opportunity data; simple clean UI.
- [ ] Section 4: Python backend, MySQL, HTML/CSS/JavaScript (chosen permitted stack).
- [ ] Section 5: accessible GitHub repository containing backend, frontend, schema,
  README and exported Postman collection; meaningful development commits;
  actual repository URL in README and submission; no credentials uploaded.
- [ ] Section 6.1: create at least three opportunities in Postman.
- [ ] Section 6.2: retrieve all.
- [ ] Section 6.3: retrieve one by ID.
- [ ] Section 6.4: update.
- [ ] Section 6.5: close.
- [ ] Section 6.6: delete.
- [ ] Section 6.7: retrieve deleted ID, show 404.
- [ ] Section 6.8: invalid/missing input, show validation response.
- [ ] Section 6: export collection, include in ZIP and repository.
- [ ] Section 7: actual video shows running backend/frontend, create/retrieve/update/
  close/delete, validation or 404, and Postman requests/responses; <=60 seconds.
- [ ] Section 8: one ZIP includes complete source, schema, collection, README,
  actual GitHub URL, actual video or video link.
- [ ] Section 8: exact ZIP name `P24 0000 NAME CLASS.zip` using supplied details.
- [ ] Section 9: individual work; both layers required; database CRUD; no hard-coded
  records; README runnable; instructor access; no secrets; <=60-second video;
  understand and adapt your work to comply with your university's originality policy.

## Simple implementation decisions

- One MySQL table. No authentication, student applications, email, or analytics.
- Flask also serves the three frontend files. Open http://127.0.0.1:5000;
  same-origin fetch means Flask-CORS and a separate frontend server are unnecessary.
- GET list returns a JSON array (including []); GET one returns an object.
  Mutations return `{message, opportunity}` or `{message, id}`. Errors return `{error}`.
- PUT permits partial changes (including status-only close), merges with the stored
  record, then validates the whole record. Empty/unknown fields are rejected.
- Zero positions is allowed. Past dates are allowed: the assignment requires a valid
  date, not a future date. Closing is explicit, not automatic when a deadline passes.
- Required strings are trimmed; positions must be an integer (not boolean/float/string);
  deadlines must be real ISO dates YYYY-MM-DD; status is case-sensitive Open/Closed.
- MySQL 8.0.16+ is required for enforced CHECK constraints. IDs are positive signed INTs.
- No live research records are seeded by the application. Example data exists only in tests.
- Repository creation, exact personal ZIP details, and an actual recorded video remain
  external dependencies until available. Never treat them as completed by inference.

The final evidence-based statuses are in VERIFICATION.md; this source checklist is
kept as the original baseline and is not a substitute for executed test results.
