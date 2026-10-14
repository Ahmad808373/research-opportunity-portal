# Final renamed-entry-point tests - 14 October 2026

The actual packaged entry point backend/portal_app.py was executed against real
MySQL 8.0.46 using a disposable research_portal_test database.

- 13 live HTTP/MySQL Python test methods passed.
- Exported Postman collection: 14 requests, 42 assertions, zero failures in Newman.
- 16 actual Chromium/Playwright frontend checks passed, including CRUD, validation,
  duplicate-submit protection, reload persistence, mobile layout, and stopped-server errors.
- All three processes returned exit code 0.

Complete API/browser transcripts and the runner summary are in this folder.
The student's actual Windows Postman GUI run also shows 42 passing tests, zero
failures and zero errors, as visible in the supplied real demonstration video.
No screenshot files are included in the final ZIP. Historical layout screenshots
remain in the GitHub repository's earlier test-evidence records.
