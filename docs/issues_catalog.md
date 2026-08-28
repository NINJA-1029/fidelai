# Comprehensive GitHub Issues Catalog

This catalog outlines all work items across the 24-hour sprint categorized by Priority (P0: Critical Demo, P1: High Value, P2: Enhancement).

---

## 1. P0 Priority Issues (Critical for 24-Hour Golden Path Demo)

### HW-001: Flutter Project Initialization and Design System Setup
- Ticket ID: `HW-001`
- Workstream: Frontend UI Platform
- Owner: High Warden
- Priority: P0
- Objective: Scaffold Flutter mobile project with Riverpod, GoRouter, monochrome styling (0px container radius, 75px full pill interactive buttons/badges), and Lucide SVG icons.
- Dependencies: None
- Inputs: `frontend/flutter_app/pubspec.yaml`
- Consumed Contracts: None
- Outputs: `frontend/flutter_app/lib/main.dart`, `app_theme.dart`, `app_router.dart`
- Produced Contracts: None
- Execution Steps:
  1. Verify Flutter environment and dependencies.
  2. Implement `AppTheme` with monochrome palette, zero radius surfaces, and pill buttons.
  3. Configure GoRouter with routes for all 7 primary screens.
- Acceptance Criteria: Application compiles and navigates between placeholder screens.
- Verification Commands: `cd frontend/flutter_app && flutter analyze`
- Definition of Done: Theme tokens and routes verified in simulator/browser.

### HW-002: Dashboard Screen and Metric Cards Implementation
- Ticket ID: `HW-002`
- Workstream: Frontend UI Platform
- Owner: High Warden
- Priority: P0
- Objective: Build information-dense dashboard displaying balance, income, expenses, active risks, and AI recommendation card.
- Dependencies: `HW-001`
- Inputs: `shared/fixtures/dashboard.json`
- Consumed Contracts: `DashboardResponse`, `FinancialState`, `RiskSignal`, `AgentResponse`
- Outputs: `frontend/flutter_app/lib/features/dashboard/dashboard_screen.dart`
- Produced Contracts: None
- Execution Steps:
  1. Build layout with Balance Header, 30-day projection pill, active risk banner, and latest AI advice card.
  2. Bind UI to local mock fixture via Riverpod provider.
  3. Style with zero radius containers and monochrome typography.
- Acceptance Criteria: Renders full dashboard data cleanly from fixture.
- Verification Commands: `flutter test test/dashboard_test.dart`
- Definition of Done: Matches design specs without overflow or layout bugs.

### HW-003: AI Advisor Screen and Evidence Display
- Ticket ID: `HW-003`
- Workstream: Frontend UI Platform
- Owner: High Warden
- Priority: P0
- Objective: Create AI Advisor screen rendering structured recommendation, reasoning prose, factual evidence metrics, and alternative actions.
- Dependencies: `HW-001`
- Inputs: `shared/fixtures/agent_response.json`
- Consumed Contracts: `AgentResponse`, `Recommendation`, `Evidence`
- Outputs: `frontend/flutter_app/lib/features/ai_advisor/ai_advisor_screen.dart`
- Produced Contracts: None
- Execution Steps:
  1. Build recommendation card with severity/priority badge.
  2. Render evidence metrics in a structured grid with threshold indicators.
  3. Render selectable alternative action cards.
- Acceptance Criteria: Displays recommendation, evidence, and confidence rating.
- Verification Commands: `flutter test test/ai_advisor_test.dart`
- Definition of Done: Fully interactive UI responsive to state updates.

### SC-001: LLMProvider Abstraction and LlamaCpp Native Integration
- Ticket ID: `SC-001`
- Workstream: Agentic AI Layer
- Owner: The Scribe
- Priority: P0
- Objective: Implement `LLMProvider` abstract base class and concrete `LlamaCppProvider` communicating with local native `llama.cpp` server.
- Dependencies: None
- Inputs: Local `llama.cpp` HTTP server endpoint (`http://localhost:8080`)
- Consumed Contracts: None
- Outputs: `backend/agent/llm_provider.py`
- Produced Contracts: `LLMProvider` Python interface
- Execution Steps:
  1. Define abstract `LLMProvider` with `generate()` method.
  2. Implement `LlamaCppProvider` with connection pooling, retries, and timeout management.
  3. Implement `MockLLMProvider` returning valid fixture strings for offline tests.
- Acceptance Criteria: `LlamaCppProvider` successfully generates text from local server; fallback activates on connection loss.
- Verification Commands: `pytest backend/tests/test_agent_tools.py`
- Definition of Done: Unit tests pass for both mock and live providers.

### SC-002: LangGraph Reasoning State Machine and Tool Orchestration
- Ticket ID: `SC-002`
- Workstream: Agentic AI Layer
- Owner: The Scribe
- Priority: P0
- Objective: Build LangGraph workflow that receives financial triggers, queries deterministic engine tools, compiles evidence, and prompts Qwen for explainable guidance.
- Dependencies: `SC-001`, `AL-003`
- Inputs: `AgentRequest`, `FinancialState`
- Consumed Contracts: `AgentRequest`, `AgentResponse`, `FinancialState`, `RiskSignal`
- Outputs: `backend/agent/graph.py`, `backend/agent/tools.py`
- Produced Contracts: `AgentResponse`
- Execution Steps:
  1. Implement deterministic tool wrappers in `tools.py`.
  2. Define LangGraph state schema containing event, state, tool outputs, and recommendation.
  3. Implement prompt template grounding Qwen in exact numerical evidence.
  4. Parse and validate LLM output into `AgentResponse` Pydantic model.
- Acceptance Criteria: LangGraph executes from trigger to valid `AgentResponse` adhering to schema.
- Verification Commands: `pytest backend/tests/test_agent_tools.py`
- Definition of Done: End-to-end graph test passing with mock and real provider.

### AL-001: Data Ingestion and Normalization Engine
- Ticket ID: `AL-001`
- Workstream: Ingestion and Normalization
- Owner: The Alchemist
- Priority: P0
- Objective: Implement transaction and SMS normalization converting unstructured strings into canonical `FinancialEvent` and `Transaction` instances.
- Dependencies: None
- Inputs: SMS notification strings, receipt JSONs, CSV lines
- Consumed Contracts: `FinancialEvent`, `Transaction`
- Outputs: `backend/ingestion/normalizer.py`, `backend/ingestion/sms_parser.py`
- Produced Contracts: `FinancialEvent`, `Transaction`
- Execution Steps:
  1. Build regex parsers for Indian banking SMS formats (HDFC, ICICI, SBI).
  2. Extract amount, transaction type, merchant, and account digits.
  3. Assign confidence scores based on parsing completeness.
- Acceptance Criteria: Correctly parses demo emergency medical SMS into `Transaction` with confidence $\ge 0.95$.
- Verification Commands: `pytest backend/tests/test_normalizer.py`
- Definition of Done: 100% passing unit tests across diverse SMS patterns.

### AL-002: FinancialState Calculator and Cash-Flow Engine
- Ticket ID: `AL-002`
- Workstream: Financial Engine
- Owner: The Alchemist
- Priority: P0
- Objective: Implement deterministic calculator for `FinancialState`, available cash, emergency fund coverage, and savings rate.
- Dependencies: `AL-001`
- Inputs: List of `Transaction`, `IncomeRecord`, `Bill`, `UserPreferences`
- Consumed Contracts: `FinancialState`, `Transaction`, `UserPreferences`
- Outputs: `backend/financial_engine/state_calculator.py`, `cashflow.py`
- Produced Contracts: `FinancialState`
- Execution Steps:
  1. Calculate liquid balance and available cash after immediate bills.
  2. Calculate fixed vs variable vs discretionary expense run-rates.
  3. Calculate emergency fund months relative to fixed expenses.
- Acceptance Criteria: Matches exact mathematical outputs defined in demo specifications.
- Verification Commands: `pytest backend/tests/test_financial_engine.py`
- Definition of Done: Clean, deterministic calculations with zero floating-point rounding errors.

### AL-003: Deterministic Forecasting and Risk Trigger Engine
- Ticket ID: `AL-003`
- Workstream: Financial Engine
- Owner: The Alchemist
- Priority: P0
- Objective: Implement 30-day balance forecast curve and deterministic detection for liquidity risks and spending spikes.
- Dependencies: `AL-002`
- Inputs: `FinancialState`, scheduled bills, recurring income
- Consumed Contracts: `Forecast`, `RiskSignal`, `OpportunitySignal`
- Outputs: `backend/financial_engine/forecasting.py`, `risk_detector.py`
- Produced Contracts: `Forecast`, `RiskSignal`, `OpportunitySignal`
- Execution Steps:
  1. Generate 30-day projection series taking upcoming obligations into account.
  2. Detect if projected balance dips below `minimum_cash_buffer`.
  3. Emit structured `RiskSignal(type="liquidity", severity="medium")`.
- Acceptance Criteria: Accurately identifies INR 5,600 buffer deficit on demo data.
- Verification Commands: `pytest backend/tests/test_financial_engine.py`
- Definition of Done: Risk signals created deterministically with impact amounts.

### KH-001: FastAPI Application Scaffolding and Pydantic Routing
- Ticket ID: `KH-001`
- Workstream: Backend Integration
- Owner: King's Hand
- Priority: P0
- Objective: Setup FastAPI server with CORS, Pydantic request/response validation, structured logging, and healthcheck route.
- Dependencies: None
- Inputs: `shared/contracts/contracts.py`
- Consumed Contracts: `APIError`, `DashboardResponse`
- Outputs: `backend/main.py`, `backend/api/routes.py`
- Produced Contracts: FastAPI router endpoints
- Execution Steps:
  1. Initialize FastAPI app with custom exception handlers.
  2. Implement `/api/v1/health` and `/api/v1/dashboard`.
  3. Wire route handlers to services and mock fixtures.
- Acceptance Criteria: Server boots and returns healthy status and validated responses.
- Verification Commands: `pytest backend/tests/test_api.py`
- Definition of Done: All routes respond with HTTP 200 and schema-valid JSON.

### KH-002: Service Orchestration and Golden Path Integration
- Ticket ID: `KH-002`
- Workstream: Backend Integration
- Owner: King's Hand
- Priority: P0
- Objective: Connect Ingestion -> Financial Engine -> LangGraph Agent -> FastAPI into a unified pipeline.
- Dependencies: `AL-001`, `AL-002`, `AL-003`, `SC-002`, `KH-001`
- Inputs: Transaction input from Flutter or API test
- Consumed Contracts: `Transaction`, `FinancialEvent`, `FinancialState`, `AgentResponse`
- Outputs: `backend/services/orchestrator.py`, `backend/tests/test_golden_path.py`
- Produced Contracts: None
- Execution Steps:
  1. Build `OrchestratorService.process_transaction()`.
  2. Update state, detect risks, invoke agent if material change occurs.
  3. Return combined payload to client.
- Acceptance Criteria: Full golden path executes in under 2 seconds.
- Verification Commands: `pytest backend/tests/test_golden_path.py`
- Definition of Done: Golden path integration test passes end-to-end.

---

## 2. P1 Priority Issues (High Value Enhancements)

### HW-004: Interactive Transactions Screen and Filter List
- Ticket ID: `HW-004`
- Owner: High Warden
- Priority: P1
- Objective: Build searchable transactions screen with source tags, confidence indicators, and categorization chips.

### HW-005: Financial Goals and Pacing Visualizer
- Ticket ID: `HW-005`
- Owner: High Warden
- Priority: P1
- Objective: Implement Goals screen displaying progress bars, target dates, and monthly pacing requirements.

### SC-003: Multi-Objective Conflict Resolution Engine
- Ticket ID: `SC-003`
- Owner: The Scribe
- Priority: P1
- Objective: Enhance agent reasoning prompts to balance competing goals (e.g. emergency fund vs aggressive investment SIP vs debt payoff).

### AL-004: What-If Simulation Engine
- Ticket ID: `AL-004`
- Owner: The Alchemist
- Priority: P1
- Objective: Implement deterministic delta calculations for simulated income or expense shocks.

### KH-003: Native AWS EC2 Provisioning and Systemd Automation
- Ticket ID: `KH-003`
- Owner: King's Hand
- Priority: P1
- Objective: Automate host setup on EC2 with native Python venv, llama.cpp service, and Nginx reverse proxy.

---

## 3. P2 Priority Issues (Optional Enhancements)

### HW-006: Investments Screen and Portfolio Breakdown
- Ticket ID: `HW-006`
- Owner: High Warden
- Priority: P2
- Objective: Render asset allocation charts and liquidity ratings for investment holdings.

### SC-004: Proactive Push Notification Generator
- Ticket ID: `SC-004`
- Owner: The Scribe
- Priority: P2
- Objective: Generate proactive short-form notification summaries for urgent liquidity warnings.

### KH-004: Supabase PostgreSQL Persistence and Alembic Migrations
- Ticket ID: `KH-004`
- Owner: King's Hand
- Priority: P2
- Objective: Implement persistent database storage and migrations for long-term historical records.
