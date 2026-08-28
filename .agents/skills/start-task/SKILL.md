---
name: start-task
description: Standardized engineering workflow skill for starting and resolving GitHub issues
---

# Start Task Workflow Skill

This skill guides a developer or agent through picking an assigned issue, establishing a feature branch, implementing according to shared contracts, running verification, and submitting a pull request.

## Step-by-Step Procedure

### Step 1: Authentication and Environment Discovery
Verify GitHub CLI authentication and retrieve current repository context:
```bash
gh auth status
git status
```

### Step 2: Retrieve Assigned Open Issues (/lmi)
List open issues assigned to the active user:
```bash
gh issue list --assignee "@me" --state open
```

### Step 3: Inspect Issue and Contracts
View the full specification of the target issue:
```bash
gh issue view <ISSUE_NUMBER>
```
Review the contracts in `shared/contracts/contracts.py` and relevant mock fixtures in `shared/fixtures/`.

### Step 4: Ensure Base Branch is Clean and Up-to-Date
Ensure you are basing changes off the active integration branch (`dev`):
```bash
git checkout dev 2>/dev/null || git checkout -b dev origin/dev 2>/dev/null || git checkout -b dev main
git pull origin dev 2>/dev/null || true
```

### Step 5: Create Issue-Linked Branch
Create and checkout a new branch following the canonical naming convention:
- For features: `git checkout -b feature/issue-<ISSUE_NUMBER>-<short-slug>`
- For bugfixes: `git checkout -b fix/issue-<ISSUE_NUMBER>-<short-slug>`

### Step 6: Implementation
- Implement the requested logic strictly within assigned directory boundaries.
- Adhere strictly to the Zero Emoji rule across all files.
- Test against mock fixtures first.

### Step 7: Atomic Commits
Commit changes atomically referencing the issue number:
```bash
git add <files>
git commit -m "feat(<scope>): concise description (issue #<ISSUE_NUMBER>)"
```

### Step 8: Run Local Verification
Run test suites to ensure zero regressions:
```bash
source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/ -v
# For frontend changes:
# cd frontend/flutter_app && flutter test
```

### Step 9: Push and Open Pull Request Targeting dev
Push the feature branch and create a PR targeting `dev` referencing the issue using the common template structure (`.github/pull_request_template.md`):
```bash
git push -u origin HEAD
gh pr create --base dev --title "feat(<scope>): implement issue #<ISSUE_NUMBER>" --template .github/pull_request_template.md
```

### Step 10: Gracefully Handle Project V2
If GitHub Project V2 is configured, update the item status to In Review; if automation fails due to API permissions, proceed without blocking.

### Step 11: Merge into dev Upon User Satisfaction
Once the user reviews and confirms satisfaction with the work:
1. Merge the PR or feature branch into `dev`:
```bash
gh pr merge --squash --delete-branch || (git checkout dev && git merge --squash feature/issue-<ISSUE_NUMBER>-<short-slug> && git commit -m "feat(<scope>): merge issue #<ISSUE_NUMBER> into dev" && git push origin dev)
```
2. Close the linked issue if not auto-closed:
```bash
gh issue close <ISSUE_NUMBER> --comment "Resolved and merged into dev."
```

### Step 12: Create or Update Dev-to-Main Release Pull Request
After clean merge into `dev`, ensure a PR exists to merge `dev` into `main` using the common template:
```bash
gh pr create --base main --head dev --title "chore(release): merge dev into main" --body "## Summary of Changes
Syncs active sprint development from dev branch into release branch main.

## Verification and Testing
All automated test suites and contract validations passed." || true
```


