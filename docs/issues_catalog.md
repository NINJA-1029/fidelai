# Comprehensive Granular GitHub Issues & Task Catalog

This catalog provides granular, minute-level specifications for all engineering tasks across the 24-hour sprint. The frontend is exclusively a **Flutter Mobile Application** (`frontend/flutter_app/`) adhering to the **Monopo Saigon** editorial design system.

---

## 1. High Warden (Frontend: Flutter Mobile Only)

### Task HW-001: Scaffold Flutter Mobile Shell, AppTheme & Monopo Saigon Tokens
- **Ticket ID:** `HW-001`
- **Workstream:** Flutter Mobile Platform
- **Owner:** High Warden
- **Priority:** P0
- **Target Files:**
  - `frontend/flutter_app/lib/main.dart`
  - `frontend/flutter_app/lib/core/theme/app_theme.dart`
  - `frontend/flutter_app/pubspec.yaml`
- **Objective:** Establish the Flutter mobile application shell with dark theme, persistent bottom navigation bar (5 tabs: `OVERVIEW`, `ADVISOR`, `LEDGER`, `GOALS`, `SIMULATE`), and exact Monopo Saigon design tokens.
- **Detailed Specifications:**
  1. `app_theme.dart`:
     - Obsidian (`#000000`), Paper (`#FFFFFF`), Inkstone (`#181818`), Felt Gray (`#6D6D6D`), Slate Pill (`#636363`), Ash Mist (`#9A9A9A`).
     - Iridescent Gradient: `LinearGradient(colors: [Color(0xFFA0E0AB), Color(0xFFFFAC2E), Color(0xFFA52D25)])`.
     - `BorderRadius.zero` for cards, dialogs, input fields, containers.
     - `BorderRadius.circular(75.0)` for buttons, chips, tags.
     - Zero icons or emojis anywhere in the layout. Pure typographic indicators.
  2. `main.dart`:
     - `MainShell` with `IndexedStack` switching between the 5 feature screens.
     - Hairline top border on bottom navigation bar.
- **Acceptance Criteria:**
  - Zero emojis or icons.
  - Clean bottom bar switching without state loss.
- **Verification Commands:** `cd frontend/flutter_app && flutter test`

---

### Task HW-002: Implement Dashboard Screen (Hero, 4 Metric Cards & Guidance)
- **Ticket ID:** `HW-002`
- **Workstream:** Flutter Mobile Platform
- **Owner:** High Warden
- **Priority:** P0
- **Target Files:**
  - `frontend/flutter_app/lib/features/dashboard/dashboard_screen.dart`
- **Objective:** Implement the Mobile Overview screen with atmospheric hero section, 2x2 metric grid, and decision guidance card.
- **Detailed Specifications:**
  1. Hero Container:
     - Obsidian background with 25% opacity iridescent gradient overlay.
     - Headline: `Preserve Liquidity. Reason Over Tradeoffs.` (32px font weight 300).
     - Full pill ghost buttons (`OPEN ADVISOR`, `SIMULATE`).
  2. 2x2 Metric Cards Grid:
     - `CURRENT BALANCE` -> `INR 30,000` (`-12,000 DEBIT`).
     - `AVAILABLE CASH` -> `INR 12,000` (`18,000 DUE 6D`).
     - `30-DAY PROJECTED` -> `INR 19,400` (`FLOOR: 25,000`).
     - `EMERGENCY FUND` -> `2.1 MO` (`INR 50,000 LIQUID`).
  3. Strategic Decision Card:
     - Recommendation title, `HIGH PRIORITY` full-pill badge, reasoning summary, tradeoff explanation, and `OPEN AI ADVISOR` action button.
- **Acceptance Criteria:**
  - Strict 0px card borders and 75px button pills.
- **Verification Commands:** `cd frontend/flutter_app && flutter test`

---

### Task HW-003: Implement AI Advisor Screen with Evidence Matrix
- **Ticket ID:** `HW-003`
- **Workstream:** Flutter Mobile Platform
- **Owner:** High Warden
- **Priority:** P0
- **Target Files:**
  - `frontend/flutter_app/lib/features/ai_advisor/ai_advisor_screen.dart`
- **Objective:** Implement the interactive AI Advisor screen with evidence matrix cards, evaluated tradeoffs, alternative action pills, and bottom query input.
- **Detailed Specifications:**
  1. Recommendation card with priority badge.
  2. 4-Card Evidence Matrix Grid (`BALANCE`, `PROJECTION`, `BUFFER`, `OBLIGATIONS`).
  3. Evaluated Tradeoffs card with bullet points.
  4. Actionable Alternatives list with full-pill `SELECT` buttons.
  5. Bottom query input bar triggering `api.getDecisionAdvice()`.
- **Acceptance Criteria:**
  - Displays complete evidence matrix and reasoning prose upon query.
- **Verification Commands:** `cd frontend/flutter_app && flutter test`

---

### Task HW-004: Implement Searchable Transaction Ledger Screen
- **Ticket ID:** `HW-004`
- **Workstream:** Flutter Mobile Platform
- **Owner:** High Warden
- **Priority:** P1
- **Target Files:**
  - `frontend/flutter_app/lib/features/transactions/transactions_screen.dart`
- **Objective:** Implement the Mobile Ledger screen with search field, horizontal category filter pills, and clean transaction cards.
- **Detailed Specifications:**
  1. Search field filtering across merchant and description.
  2. Category filter pills: `ALL`, `INCOME`, `HOUSING`, `GROCERIES`, `UNEXPECTED`.
  3. Card list displaying timestamp, category tag, description, monospaced amount (`-INR 12,000.00`, `+INR 65,000.00`), and source confidence.
- **Acceptance Criteria:**
  - Filters update instantaneously.
- **Verification Commands:** `cd frontend/flutter_app && flutter test`

---

### Task HW-005: Implement Goals & Pacing Visualizer Screen
- **Ticket ID:** `HW-005`
- **Workstream:** Flutter Mobile Platform
- **Owner:** High Warden
- **Priority:** P1
- **Target Files:**
  - `frontend/flutter_app/lib/features/goals/goals_screen.dart`
- **Objective:** Implement the Financial Goals screen displaying active goals, progress bars, and monthly pacing requirements.
- **Detailed Specifications:**
  1. Cards for `EMERGENCY FUND RESERVE` and `ANNUAL FAMILY VACATION`.
  2. Binary monochrome `LinearProgressIndicator` (0px radius).
  3. Monthly pacing metric (e.g. `INR 5,500/mo`) and deadline date.
- **Acceptance Criteria:**
  - Clean hairline cards with 0px radius.
- **Verification Commands:** `cd frontend/flutter_app && flutter test`

---

### Task HW-006: Implement What-If Simulation Calculator Screen
- **Ticket ID:** `HW-006`
- **Workstream:** Flutter Mobile Platform
- **Owner:** High Warden
- **Priority:** P1
- **Target Files:**
  - `frontend/flutter_app/lib/features/simulation/simulation_screen.dart`
- **Objective:** Implement the What-If simulation calculator screen with amount input and trajectory comparison output card.
- **Detailed Specifications:**
  1. Shock parameter card with amount text field and `CALCULATE TRAJECTORY` button.
  2. Projected Impact card showing `BASELINE (30-DAY)` vs `SIMULATED (POST-SHOCK)` and violation badge.
- **Acceptance Criteria:**
  - Displays buffer violation status (`BUFFER VIOLATION` vs `BUFFER PRESERVED`).
- **Verification Commands:** `cd frontend/flutter_app && flutter test`

---

### Task HW-007: Implement ApiClient & Riverpod State Providers
- **Ticket ID:** `HW-007`
- **Workstream:** Flutter Mobile Platform
- **Owner:** High Warden
- **Priority:** P1
- **Target Files:**
  - `frontend/flutter_app/lib/core/network/api_client.dart`
  - `frontend/flutter_app/lib/core/models/models.dart`
- **Objective:** Build the Dio HTTP client connecting to FastAPI `http://localhost:8000/api/v1` with fallback mock data.
- **Detailed Specifications:**
  1. `getFinancialState(userId)` -> `FinancialStateModel`.
  2. `getDecisionAdvice(userId, query)` -> `AgentResponseModel`.
  3. Graceful offline fallback on connection timeout.
- **Acceptance Criteria:**
  - Returns deterministic models when local backend is unreachable.
- **Verification Commands:** `cd frontend/flutter_app && flutter test`

---

## 2. The Scribe (AI & Agentic Reasoning)

### Task SC-001: Implement `LLMProvider` Abstraction & Native `LlamaCppProvider`
- **Ticket ID:** `SC-001`
- **Workstream:** Agentic AI Layer
- **Owner:** The Scribe
- **Priority:** P0
- **Target Files:**
  - `backend/agent/llm_provider.py`
  - `backend/agent/__init__.py`
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_agent_tools.py`

---

### Task SC-002: Build LangGraph Workflow with Self-Correction & Fallback
- **Ticket ID:** `SC-002`
- **Workstream:** Agentic AI Layer
- **Owner:** The Scribe
- **Priority:** P0
- **Target Files:**
  - `backend/agent/graph.py`
  - `backend/agent/tools.py`
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_agent_tools.py`

---

### Task SC-003: Implement Multi-Objective Tradeoff Reasoning & Alternatives
- **Ticket ID:** `SC-003`
- **Workstream:** Agentic AI Layer
- **Owner:** The Scribe
- **Priority:** P1
- **Target Files:**
  - `backend/agent/graph.py`
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_agent_tools.py`

---

## 3. The Alchemist (Financial Engine & Ingestion)

### Task AL-001: Implement Indian Banking SMS Regex Parser & Normalizer
- **Ticket ID:** `AL-001`
- **Workstream:** Ingestion and Normalization
- **Owner:** The Alchemist
- **Priority:** P0
- **Target Files:**
  - `backend/ingestion/sms_parser.py`
  - `backend/ingestion/normalizer.py`
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_normalizer.py`

---

### Task AL-002: Implement Deterministic `FinancialStateCalculator`
- **Ticket ID:** `AL-002`
- **Workstream:** Financial Engine
- **Owner:** The Alchemist
- **Priority:** P0
- **Target Files:**
  - `backend/financial_engine/state_calculator.py`
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_financial_engine.py`

---

### Task AL-003: Implement Trajectory Forecaster & Deterministic Risk Detector
- **Ticket ID:** `AL-003`
- **Workstream:** Financial Engine
- **Owner:** The Alchemist
- **Priority:** P0
- **Target Files:**
  - `backend/financial_engine/forecasting.py`
  - `backend/financial_engine/risk_detector.py`
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_financial_engine.py`

---

## 4. King's Hand (Backend, Integration & DevOps)

### Task KH-001: Setup FastAPI Application, Validation & Routing Layer
- **Ticket ID:** `KH-001`
- **Workstream:** Backend Integration
- **Owner:** King's Hand
- **Priority:** P0
- **Target Files:**
  - `backend/main.py`
  - `backend/api/routes.py`
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_api.py`

---

### Task KH-002: Build End-to-End Orchestrator Pipeline & Golden Path Test
- **Ticket ID:** `KH-002`
- **Workstream:** Backend Integration
- **Owner:** King's Hand
- **Priority:** P0
- **Target Files:**
  - `backend/services/orchestrator.py`
  - `backend/tests/test_golden_path.py`
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_golden_path.py`

---

### Task KH-003: Native AWS EC2 Provisioning & Systemd Automation
- **Ticket ID:** `KH-003`
- **Workstream:** Backend Integration / DevOps
- **Owner:** King's Hand
- **Priority:** P1
- **Target Files:**
  - `deployment/aws/fastapi.service`
  - `deployment/aws/llamacpp.service`
  - `deployment/aws/nginx.conf`
  - `deployment/aws/setup_ec2.sh`
- **Verification Commands:** `bash -n deployment/aws/setup_ec2.sh`
