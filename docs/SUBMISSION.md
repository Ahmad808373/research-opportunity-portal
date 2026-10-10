# Submission remains pending

The working package contains the implemented source, schema, Postman export,
README, documentation, test evidence, and a separate real Git history bundle.
It is named `research-opportunity-portal_WORKING_PACKAGE.zip`, deliberately not
the final personal assignment ZIP.

## Missing items that must be completed

1. Confirm the published project remains accessible to the instructor at the
   actual GitHub URL. Milestone publishing is being finalized in this package.
2. Run the project on your Windows computer and demonstrate the imported collection
   in Postman desktop. The same collection has already passed in Newman here.
3. Record the real demonstration using DEMO_PLAN.md; verify duration <=60 seconds.
4. Supply your exact registration number, full submission name, and class. Do not
   infer the class or registration number from a PDF heading or older conversation.
5. Include demo.mp4 or an accessible video URL before making the final submission ZIP.

## Final ZIP contents

- backend source, requirements, and .env.example (placeholders only)
- frontend HTML/CSS/JavaScript
- database/schema.sql
- exported Postman collection
- README with the actual repository URL and accurate setup/run instructions
- GITHUB_LINK.txt with https://github.com/Ahmad808373/research-opportunity-portal
- demo.mp4 or VIDEO_LINK.txt with an actual instructor-accessible video URL
- Optional docs/tests and supporting evidence

The Git history bundle is useful for recovery/publication and may be left out of
the final instructor ZIP once GitHub commits are verified. Do not include .git,
.venv, .env, database data directories, node_modules, tokens, or local logs.

Name the final archive exactly in the PDF's format:
`P24 0000 NAME CLASS.zip`, using your supplied actual details. The generic working
package must not be submitted unchanged while required items are pending.

## PowerShell packaging procedure after missing items are complete

From the project root, with your real video copied to `demo.mp4` (or a real URL
saved in VIDEO_LINK.txt):

```powershell
$stage = Join-Path $env:TEMP ("portal-submission-" + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $stage | Out-Null
New-Item -ItemType Directory -Path "$stage\backend" | Out-Null
Copy-Item backend\app.py,backend\db.py,backend\requirements.txt,backend\.env.example "$stage\backend"
Copy-Item frontend,database,postman,docs -Destination $stage -Recurse
New-Item -ItemType Directory -Path "$stage\tests" | Out-Null
Copy-Item tests\test_api.py,tests\test_frontend.cjs "$stage\tests"
Copy-Item README.md,.gitignore,GITHUB_LINK.txt -Destination $stage
if (Test-Path demo.mp4) { Copy-Item demo.mp4 $stage }
elseif (Test-Path VIDEO_LINK.txt) { Copy-Item VIDEO_LINK.txt $stage }
else { throw "Add your actual video or video link before packaging." }
$zipName = Read-Host "Enter the exact final filename: P24 0000 NAME CLASS.zip using your details"
if (-not $zipName.EndsWith('.zip')) { throw "Filename must end in .zip" }
if (Test-Path $zipName) { throw "That ZIP already exists. Choose a new path or inspect it first." }
Compress-Archive -Path "$stage\*" -DestinationPath $zipName
```

Open the ZIP and confirm all required files are present, no secrets are included,
the repository contains the source, and the video plays within the time limit.
The temporary stage remains available for review; remove that specific stage
after checking the archive if desired. Never zip the whole working directory blindly.
