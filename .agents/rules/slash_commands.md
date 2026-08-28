# Slash Commands and Shortcuts

## `/lmi` (List My Issues)
When the user types `/lmi` (or requests "list my issues"):
1. Query GitHub for only the issues assigned to the authenticated user using `gh issue list --assignee "@me" --state open`.
2. Do NOT list issues assigned to other team members or unassigned issues.
3. Display only the user's assigned issues in a clean, concise markdown table including:
   - Issue number (linked if applicable)
   - Issue tag/identifier (e.g. `HW-001`, `HW-002`, etc.)
   - Issue title
   - State (`OPEN`)
4. Ask the user which of their assigned issues they would like to work on next.
