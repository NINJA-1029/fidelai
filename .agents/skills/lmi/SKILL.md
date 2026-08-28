---
name: lmi
description: Lists exclusively the GitHub issues assigned to the currently authenticated user
---

# List My Issues (`/lmi`)

This workflow retrieves and displays only the open GitHub issues assigned to the active user.

## Procedure

1. Run the GitHub CLI command:
   ```bash
   gh issue list --assignee "@me" --state open
   ```
2. Parse and format the output into a clean table containing:
   - Issue Number
   - Tag/Identifier (e.g., `HW-001`)
   - Title
   - State
3. Do not output issues belonging to other assignees.
4. Prompt the user for which assigned issue to tackle.
