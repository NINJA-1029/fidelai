# AGENTS.md - Agentic AI Financial Management System Operational Protocol

## 1. System Mission and Operating Mandate

This repository houses an Agentic AI Financial Management System engineered to ingest heterogeneous financial data, compute a deterministic financial state, detect proactive risks and opportunities, and deliver explainable decision support via an LLM reasoning engine backed by Qwen GGUF running natively on llama.cpp.

This project is executed under a strict 24-hour development sprint with four dedicated developers working in parallel. The goal is to establish the smallest technically sound, end-to-end operational system without unnecessary infrastructure complexity.

### Primary Data Flow (The Golden Path)

Heterogeneous Financial Input
    |
    v
Input Normalization
    |
    v
Financial Event
    |
    v
Financial State Update
    |
    v
Deterministic Financial Analytics
    |
    +-------------------+-------------------+
    |                                       |
    v                                       v
Risk Detection                         Opportunity Detection
    |                                       |
    +-------------------+-------------------+
                        |
                        v
                 LangGraph Workflow
                        |
           +------------+------------+
           |                         |
           v                         v
Deterministic Tools             Qwen Reasoning (llama.cpp)
           |                         |
           +------------+------------+
                        |
                        v
          Explainable Recommendation & Evidence
                        |
                        v
                  FastAPI Layer
                        |
                        v
              Flutter Mobile Application

---

## 2. Absolute Prohibitions

### Absolute Emoji and Icon Prohibition
There is an absolute prohibition on emojis and icons across this entire repository and UI.
- No emojis in source code, docstrings, comments, documentation, Git commits, branch names, issue templates, logs, test fixtures, or UI components.
- No decorative icons, icon packs, or glyph clutter in UI components or labels. Use confident, minimalist typographic labels and monospaced indicators instead.

### Strict Color Discipline Prohibition
- Pure monochrome palette: Obsidian (`#000000`), Paper (`#ffffff`), Inkstone (`#181818`), Felt Gray (`#6d6d6d`), Slate Pill (`#636363`), Ash Mist (`#9a9a9a`).
- No unnecessary colors, colorful badges, or gradient fills in UI controls. The iridescent gradient is restricted exclusively to atmospheric hero media.

### Absolute Container and Orchestration Prohibition
- Do not use Docker.
- Do not use Kubernetes.
- Do not create Dockerfiles, docker-compose files, Helm charts, ECS/EKS manifests, or container registries.
- All services execute natively on host OS environments (macOS/Linux locally, EC2 Ubuntu instances on AWS).

### Absolute Prohibition on LLM Arithmetic
- The LLM is never the calculator or source of truth for financial math.
- All calculations (cash flow, liquidity, goal pacing, risk scores, forecasts) are calculated deterministically by the Financial Engine.
- The LLM reasons over structured facts and evidence provided by deterministic tools.

---

## 3. Developer Ownership and Directory Boundaries

There are four designated development roles. These codenames are strictly internal and must never be displayed in the user-facing UI.

### Dev 1: High Warden (@NINJA-1029) — Flutter Mobile Platform
- Primary Ownership: `frontend/flutter_app/`
- Assigned Issues: `#1 (HW-001)`, `#2 (HW-002)`, `#3 (HW-003)`, `#11 (HW-004)`, `#12 (HW-005)`, `#13 (HW-006)`, `#14 (HW-007)`
- Responsibilities: Flutter application, Riverpod state management, Monopo Saigon design system (0px container radius, 75px full pill buttons/badges), Overview dashboard, transactions screen, goals pacing screen, simulation screen, AI advisor screen, API client integration.
- Boundary: Must consume shared contracts. Must not implement financial math or duplicate backend engine logic.

### Dev 2: The Scribe (@Indhracha-05) — AI / Agentic Workflow
- Primary Ownership: `backend/agent/`
- Assigned Issues: `#4 (SC-001)`, `#5 (SC-002)`, `#15 (SC-003)`
- Responsibilities: LangGraph state machine, LLMProvider abstraction, llama.cpp GGUF client integration, deterministic tool execution, evidence compilation, recommendation synthesis, uncertainty reasoning, proactive risk analysis, structured AgentResponse validation.
- Boundary: Must not perform financial arithmetic; must call deterministic tools.

### Dev 3: The Alchemist (@babi-13) — Financial Engine + Datasets
- Primary Ownership: `backend/financial_engine/`, `backend/ingestion/`, `shared/fixtures/`
- Assigned Issues: `#6 (AL-001)`, `#7 (AL-002)`, `#8 (AL-003)`
- Responsibilities: Ingestion normalizers (SMS regex, receipts, CSV, bank feeds), FinancialEvent generation, FinancialState calculator, cash-flow analysis, forecasting engine, risk/opportunity detection, goal progress math, uncertainty scoring, demo dataset scenarios.
- Boundary: Owns the mathematical and statistical source of truth.

### Dev 4: King's Hand (@rakshithshakkthi) — Backend + Cloud + Integration
- Primary Ownership: `backend/api/`, `backend/models/`, `backend/repositories/`, `backend/services/`, `deployment/`
- Assigned Issues: `#9 (KH-001)`, `#10 (KH-002)`, `#16 (KH-003)`
- Responsibilities: FastAPI application, Pydantic schemas, PostgreSQL/Supabase database models, repository layer, endpoint orchestration, end-to-end integration, native AWS EC2 deployment automation, CI/CD, final merge authority.
- Boundary: Ensures architectural integrity and unblocks parallel tracks.

---

## 4. Contract-First and Mock-First Development

Parallel development relies on explicit, immutable shared contracts and fixtures.

1. All data exchanged between modules must conform to schemas in `shared/contracts/contracts.py` and `shared/schemas/`.
2. Mock fixtures in `shared/fixtures/` serve as independent testbeds for all developers:
   - `transactions.json`: Raw transaction payloads.
   - `financial_events.json`: Normalized financial events.
   - `financial_state.json`: Complete canonical financial state.
   - `agent_request.json`: Payload passed to LangGraph agent.
   - `agent_response.json`: Structured recommendation output.
   - `dashboard.json`: Aggregated dashboard response.
   - `simulation.json`: What-if scenario request and response.
3. No developer may block on another developer's implementation. Build against fixtures, then connect live endpoints during integration milestones.

---

## 5. UI Design System Principles

- Monochrome-First: Neutral dark/light slate tones. Semantic accents (red/amber/green) used strictly for status indicators and risk levels.
- Zero Radius Rule: Containers, text inputs, cards, tables, modal dialogs use 0px border radius (sharp geometric aesthetics).
- Pill Rule: Interactive buttons and category/status badges use 75px full pill border radius.
- Typography: Clean sans-serif (Inter, Roboto, or system sans).
- Iconography: Lucide SVG icons or standard Flutter vector icons. No emoji graphics.
- Information Density: High financial density, clean tables, clear metrics, deterministic charts using fl_chart.

---

## 6. Uncertainty and Data Quality Model

All ingested financial metrics and state variables must support explicit uncertainty:
- `confirmed`: Fully verified by authoritative institution or settled ledger.
- `estimated`: Derived via deterministic extrapolation or verified pattern.
- `uncertain`: Extracted with low confidence or variable income stream.
- `unknown`: Missing information; system must explicitly acknowledge lack of data rather than fabricating values.

---

## 7. Git and Contribution Workflow

### Branch Structure
- `main`: Protected release branch holding production-stable releases.
- `dev`: Central integration branch for ongoing sprint development. All feature and fix branches branch from and merge into `dev`.

### Branch Naming Convention
- Feature branches: `feature/issue-<NUMBER>-<short-slug>`
- Bug fix branches: `fix/issue-<NUMBER>-<short-slug>`

### Commit Message Standards
- Must be atomic, descriptive, and reference the associated issue.
- Format: `feat(scope): concise description (issue #<NUMBER>)` or `fix(scope): concise description (issue #<NUMBER>)`
- Strictly zero emojis in commit messages.

### Common Pull Request Template
- All developers must adhere to the standardized PR template in `.github/pull_request_template.md`.
- Required sections: Summary of Changes, Associated Issue, Workstream and Role, Contracts and Fixtures Impacted, Verification and Testing, and Quality Checklist.

### Pull Request Rules
- Feature PR target branch: All task PRs must target the `dev` branch (`--base dev`).
- PR title must include issue reference: `feat(<scope>): description (issue #<NUMBER>)`.
- PR must pass all unit and contract tests before review.
- Manual User Review & Merge: Agents open the Pull Request from the feature branch to `dev` and submit it for user review. The user personally compares the diff and merges the PR into `dev`. Agents must never auto-merge or create PRs into `main`.
- King's Hand / Maintainer has final review and merge authority for cross-cutting changes.

---

## 8. 24-Hour Timeline and Milestones

- Hour 0-1: Architecture, contracts, repository scaffolding, issue assignment.
- Hour 1-6: Parallel module development against fixtures (Flutter UI, Agent LangGraph, Financial Engine, FastAPI).
- Hour 6-10: First Vertical Slice Integration (Transaction -> Event -> State -> Risk -> Agent -> FastAPI -> Flutter).
- Hour 10-14: Advanced intelligence (proactive triggers, balance forecasting, goal optimization, uncertainty scoring).
- Hour 14-18: What-if simulation engine, AWS EC2 native deployment, remote API integration.
- Hour 18-21: Feature Freeze; end-to-end stabilization, edge-case hardening, unit/integration test coverage.
- Hour 21-24: Final demonstration polish, fallback fixture validation, presentation delivery.
