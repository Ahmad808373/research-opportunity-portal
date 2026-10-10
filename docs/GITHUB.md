# GitHub repository and milestone workflow

Repository: https://github.com/Ahmad808373/research-opportunity-portal

The repository is public. Initial write attempts returned HTTP 403 even though
account metadata reported push/admin. After Ahmad corrected the connector permissions,
actual branch creation and a small file write succeeded. The development branch
and write-check commit af9b1bbda89173baaa40d23aab7e7643565d04fd were read back.
The verification file is docs/github-write-check.txt. No credentials were uploaded.

Milestones are published individually and verified by reading the actual remote
branch head. Both main and development receive the same commit. The original
GitHub initial commit is preserved. Previously blocked local commits are published
in their original milestone order; they were not claimed as pushed while access failed.
The verified source commit log is in GITHUB_COMMITS.json once publication finishes.

## Continue locally on Windows

Use Git for Windows. Clone the actual remote history:

```powershell
git clone https://github.com/Ahmad808373/research-opportunity-portal.git
cd research-opportunity-portal
git config user.name "Ahmad Abdullah"
git config user.email "180828679+Ahmad808373@users.noreply.github.com"
```

Use main for this individual assignment, or check out development if desired.
Follow README.md to create a virtual environment and your local .env. Git for
Windows can open a browser to sign in during an authenticated push; never put a
token into the remote URL or send credentials in chat.

After each meaningful change:

```powershell
git status
git add backend frontend database postman tests docs README.md .gitignore
git diff --cached
git commit -m "Describe the completed milestone"
git push origin main
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Compare the final two hashes to verify the push. Do not stage your real .env or
credentials. Inspect the staged diff even though .gitignore excludes common secret
paths. If a push is rejected, inspect/fetch the remote changes and resolve them;
do not force-push over another change.

The working ZIP includes a Git bundle as a recovery copy of the actual published
history. Normal development should use the GitHub clone above. To inspect the
bundle independently, run `git clone research-opportunity-portal-history.bundle
portal-history-copy` from the package parent directory. Configure origin to the
actual GitHub URL if you use that copy for later work.

For submission, open the public repository while signed out and check all required
files are visible. The instructor must be able to access it. The repository URL is
also in README.md and GITHUB_LINK.txt.
