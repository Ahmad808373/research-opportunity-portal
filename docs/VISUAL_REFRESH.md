# Frontend visual refresh - 14 October 2026

The portal now uses a forest-green and warm ivory palette, serif display headings,
a self-contained research illustration, clearer opportunity cards with description
previews, improved full-detail presentation, and a coordinated create/edit form.
The illustration is inline SVG; typography uses installed system fonts. No new
runtime dependency or external font/image service is required.

Changed application files: frontend/index.html, frontend/style.css, frontend/script.js.
API endpoints, MySQL schema, and local configuration are unchanged. Opportunity
content still comes from the live Flask/MySQL API. The JavaScript changes add
presentation elements only: card descriptions and the empty details panel.

## Verified after the refresh

- All 16 existing Playwright frontend checks passed against real Flask/MySQL:
  create, retrieve/details, update, close, delete/cancel, required/whitespace/
  positions/date validation, repeated submits, persistence after reload, safe
  HTML-like text, stopped-backend messages, and no uncaught JavaScript errors.
- Additional layout checks passed at 320, 390, 768, 1024, and 1440 pixels.
- The create dialog fits a 390px mobile viewport and Save remains reachable.
- Desktop, mobile, empty-state, and form screenshots were inspected internally.
- Three example records were created through the live API in a disposable test
  database for visual inspection; they are not seeded application data and do
  not represent actual faculty/opportunity listings.
- Database persistence after a real MySQL stop/start also passed in the harness.

Text/JSON execution evidence is in docs/visual-refresh. These tests ran in the
Linux development environment, not on the user's Windows machine. API code was
unchanged, so the complete backend and Postman suites were not rerun for styling.

## Install on the user's Windows computer

If using a Git clone, run git pull --ff-only origin main from the project folder.
If using a downloaded project, copy all three files from the frontend update ZIP
into the existing project's frontend folder and replace the old files. Do not
replace backend/.env or database files. Preserve the confirmed local DB_PORT=3307.
Start MySQL and Flask as before, open http://127.0.0.1:5000/, and press Ctrl+F5 to
refresh cached CSS and JavaScript. No database setup needs to be repeated.
