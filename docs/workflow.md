# Engineering Workflow and Collaboration Protocol

## 1. Operating Rules for Parallel Development

With four developers working simultaneously across a 24-hour sprint, isolation and contract adherence are mandatory.

### Team Roles and Workstreams
- High Warden (Dev 1): Frontend (Flutter, Riverpod, GoRouter, screens, charts, contracts consumption).
- The Scribe (Dev 2): Agentic Workflow (LangGraph, tool registration, Qwen LLMProvider, evidence synthesis).
- The Alchemist (Dev 3): Financial Engine & Datasets (Normalization, state math, risk triggers, forecast model).
- King's Hand (Dev 4): Backend, Database & Integration (FastAPI, SQLAlchemy, Supabase, EC2 deployment, CI/CD).

---

## 2. GitHub Issue Lifecycle and `/start-task` Skill

Developers initiate every work item using the `/start-task` skill:

1. Retrieve Assigned Issue: Select from open GitHub issues.
2. Read Specification: Review inputs, consumed contracts, execution steps, and acceptance criteria.
3. Branch Creation: Auto-checkout branch `feature/issue-<NUMBER>-<slug>` or `fix/issue-<NUMBER>-<slug>`.
4. Mock-First Implementation: Develop and verify against `shared/fixtures/` before integration.
5. Atomic Commits: Commit changes using format `feat(scope): description (issue #<NUMBER>)`.
6. Run Verification: Execute local test suites (`pytest`, `flutter test`).
7. Create Pull Request: Submit PR linking the issue ID.

---

## 3. Pull Request Review and Merge Gate

King's Hand is the final integration authority.
A PR will only be merged if:
1. All automated tests pass (`pytest backend/tests/`).
2. No contract schemas in `shared/contracts/` have been modified without multi-developer signoff.
3. No emojis exist in code, comments, or documentation.
4. No container artifacts (Docker/Kubernetes) have been added.
5. Code strictly adheres to directory boundaries.
