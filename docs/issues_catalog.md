# Comprehensive Granular GitHub Issues & Task Catalog

This catalog provides granular, minute-level specifications for all engineering tasks across the 24-hour sprint. Every issue defines exact file paths, function signatures, data models, execution steps, and verification commands.

---

## 1. High Warden (Frontend: Web & Mobile)

### Task HW-001: Scaffold Layout Shell, Navigation & Monopo Saigon Tokens
- **Ticket ID:** `HW-001`
- **Workstream:** Frontend UI Platform
- **Owner:** High Warden
- **Priority:** P0
- **Target Files:**
  - `frontend/web/app/layout.tsx`
  - `frontend/web/components/navigation/sidebar.tsx`
  - `frontend/web/app/globals.css`
  - `frontend/web/tailwind.config.ts`
- **Objective:** Establish the persistent application shell with a 1078px max-width centered container, 64px width left navigation sidebar, rotating circular typographic badge, and exact Monopo Saigon design tokens.
- **Detailed Specifications:**
  1. `globals.css`: Define custom properties:
     - `--color-obsidian: #000000`, `--color-paper: #ffffff`, `--color-inkstone: #181818`, `--color-felt-gray: #6d6d6d`, `--color-slate-pill: #636363`, `--color-ash-mist: #9a9a9a`.
     - `--gradient-iridescent-fade: linear-gradient(90deg, rgb(160, 224, 171), rgb(255, 172, 46) 50%, rgb(165, 45, 37))`.
     - `--ease-patient: cubic-bezier(0.19, 1, 0.22, 1)`.
  2. `sidebar.tsx`:
     - Render brand wordmark: `FIDEL` (18px, weight 400) + `AUTONOMOUS INTELLIGENCE` (11px, Felt Gray).
     - Render text links with 0px radius: `OVERVIEW (01)`, `AI ADVISOR (02)`, `LEDGER (03)`, `GOALS & PACING (04)`, `WHAT-IF SIMULATION (05)`.
     - Render rotating SVG badge (`AUTONOMOUS · FIDEL AGENT ·`) rotating at 24s linear loop. Zero icons.
  3. `layout.tsx`:
     - Wrap child pages in `max-w-[1078px] mx-auto px-12 py-16 space-y-[46px]`.
- **Acceptance Criteria:**
  - Zero icons or emojis anywhere in the layout.
  - Sidebar renders cleanly without layout shift on all desktop viewports.
  - Active route highlighted with subtle neutral background (`bg-muted`).
- **Verification Commands:** `cd frontend/web && npm run build`

---

### Task HW-002: Build Iridescent Hero & 4-Column Metric Grid
- **Ticket ID:** `HW-002`
- **Workstream:** Frontend UI Platform
- **Owner:** High Warden
- **Priority:** P0
- **Target Files:**
  - `frontend/web/app/page.tsx`
  - `frontend/web/components/ui/card.tsx`
  - `frontend/web/components/ui/button.tsx`
- **Objective:** Implement the Overview Dashboard hero environment and the 4-column canonical liquidity metrics row.
- **Detailed Specifications:**
  1. Hero Environment:
     - Full-width black surface `#000000` with 40% opacity fluid animated gradient overlay (`.iridescent-hero`).
     - Display headline: `Preserve Liquidity. Reason Over Tradeoffs.` (72px weight 300 / 400).
     - Ghost pill action buttons with 11px vertical, 33px horizontal padding, 75px radius, 1px white border (`Button variant="ghost-dark"`).
  2. Metric Cards Grid (4 Columns, equal width, 16px gap, 34px padding):
     - Card 1: `CURRENT LIQUID BALANCE` -> `INR 30,000.00` (Delta annotation: `-12,000.00 RECENT DEBIT`).
     - Card 2: `AVAILABLE (NET OF BILLS)` -> `INR 12,000.00` (Annotation: `18,000.00 DUE IN 6 DAYS`).
     - Card 3: `30-DAY PROJECTED CASH` -> `INR 19,400.00` (Annotation: `FLOOR: INR 25,000.00`).
     - Card 4: `EMERGENCY FUND` -> `2.1 MONTHS` (Annotation: `INR 50,000.00 LIQUID`).
  3. Visual Styling:
     - Sharp 0px corners on cards, hairline 1px border (`border-border`), no shadow elevation.
- **Acceptance Criteria:**
  - Strict monochrome numerals with monospaced font styling.
  - Zero icons. Pure typographic indicators.
- **Verification Commands:** `cd frontend/web && npm run build`

---

### Task HW-003: Implement Decision Guidance & Ledger Sections on Overview
- **Ticket ID:** `HW-003`
- **Workstream:** Frontend UI Platform
- **Owner:** High Warden
- **Priority:** P0
- **Target Files:**
  - `frontend/web/app/page.tsx`
  - `frontend/web/components/ui/table.tsx`
- **Objective:** Implement Section 03 (Strategic Decision Support Card) and Section 04 (Recent Transactions Table) on the overview dashboard.
- **Detailed Specifications:**
  1. Decision Guidance Card:
     - Header with title: `Preserve Near-Term Liquidity` and pill badge `[ HIGH PRIORITY ]`.
     - Reasoning prose explaining unexpected expense and upcoming obligations impact.
     - 3-Column Evidence Subgrid:
       - Evidence 1: `INR 19,400.00` (30-day forecast).
       - Evidence 2: `INR 25,000.00` (User buffer threshold).
       - Evidence 3: `INR 18,000.00` (Obligations due in 6 days).
     - Bottom Tradeoff Bar: `Tradeoff Resolved: Retained INR 140,000 investment portfolio compounding while pausing secondary Vacation Goal pacing.` + `OPEN ADVISOR` ghost pill button.
  2. Transaction Table:
     - Columns: `Date`, `Description`, `Category`, `Source`, `Confidence`, `Amount`.
     - Zero radius, clean border rows, monospaced currency alignment (`-INR 12,000.00`, `+INR 65,000.00`).
- **Acceptance Criteria:**
  - Table and card layouts adhere strictly to 0px container radius.
  - Zero emojis or icons.
- **Verification Commands:** `cd frontend/web && npm run build`

---

### Task HW-004: Implement Interactive AI Advisor Interface
- **Ticket ID:** `HW-004`
- **Workstream:** Frontend UI Platform
- **Owner:** High Warden
- **Priority:** P0
- **Target Files:**
  - `frontend/web/app/advisor/page.tsx`
  - `frontend/web/app/api/advisor/route.ts`
- **Objective:** Build the interactive AI advisor chat and decision inspection interface with real-time evidence matrix rendering and alternative action triggers.
- **Detailed Specifications:**
  1. Chat history container rendering assistant recommendations and user queries.
  2. Assistant Card structure:
     - Header: `Fidel Strategic Reasoning` + `CONFIDENCE: 94%`.
     - Recommendation banner with high-priority badge.
     - 4-Column Evidence Matrix cards (`BALANCE`, `PROJECTION`, `BUFFER`, `OBLIGATIONS`).
     - Evaluated Tradeoffs block with monospaced bullet points.
     - Actionable Alternatives list with selectable `SELECT` ghost pill buttons.
  3. Query Input Bar:
     - Monospaced input field + `SUBMIT` pill button.
     - Submits query to `/api/v1/agent/analyze` or `/api/advisor` endpoint.
- **Acceptance Criteria:**
  - Displays complete evidence matrix and reasoning prose upon response.
  - Handles network errors gracefully with deterministic fallback mock.
- **Verification Commands:** `cd frontend/web && npm run build`

---

### Task HW-005: Implement Searchable Transaction Ledger View
- **Ticket ID:** `HW-005`
- **Workstream:** Frontend UI Platform
- **Owner:** High Warden
- **Priority:** P1
- **Target Files:**
  - `frontend/web/app/transactions/page.tsx`
- **Objective:** Build the dedicated Transaction Ledger screen with real-time search, category pill filter buttons, and confidence indicators.
- **Detailed Specifications:**
  1. Search input filtering across merchant, description, and category.
  2. Category filter pills (`ALL`, `INCOME`, `HOUSING`, `GROCERIES`, `UNEXPECTED`).
  3. Tabular view with fields: `Transaction ID`, `Date`, `Description`, `Category`, `Source`, `Confidence`, `Amount`.
  4. Monospaced right-aligned monetary amounts.
- **Acceptance Criteria:**
  - Filters update instantaneously without page reload.
  - Zero icons; pure typographic badges.
- **Verification Commands:** `cd frontend/web && npm run build`

---

### Task HW-006: Implement Goals & Pacing Visualizer
- **Ticket ID:** `HW-006`
- **Workstream:** Frontend UI Platform
- **Owner:** High Warden
- **Priority:** P1
- **Target Files:**
  - `frontend/web/app/goals/page.tsx`
- **Objective:** Implement the Financial Goals screen displaying active goals, progress bars, monthly pacing run-rates, and at-risk advisory flags.
- **Detailed Specifications:**
  1. Render 2-column grid of goal cards (e.g. `Emergency Fund Reserve`, `Annual Family Vacation`).
  2. Monochrome progress bar with percentage indicator.
  3. Subgrid showing `MONTHLY PACING` (e.g. `INR 5,500/mo`) and `TARGET DEADLINE` (e.g. `2026-12-31`).
  4. Status annotation (e.g. `ON TRACK`, `AT RISK // PAUSE RECOMMENDED`).
- **Acceptance Criteria:**
  - Clean hairline cards with 0px radius.
- **Verification Commands:** `cd frontend/web && npm run build`

---

### Task HW-007: Implement Interactive What-If Scenario Simulator
- **Ticket ID:** `HW-007`
- **Workstream:** Frontend UI Platform
- **Owner:** High Warden
- **Priority:** P1
- **Target Files:**
  - `frontend/web/app/simulation/page.tsx`
- **Objective:** Implement the What-If simulation calculator view with scenario selection, amount delta inputs, and trajectory comparison output cards.
- **Detailed Specifications:**
  1. Left Column (1/3 width): Parameter form with `SCENARIO TYPE` select, `AMOUNT (INR)` input, `DESCRIPTION` input, and `RUN SIMULATION` button.
  2. Right Column (2/3 width): Result card showing `BASELINE 30-DAY PROJECTED` vs `SIMULATED POST-SHOCK`, impact summary, and strategic decision guidance.
  3. Calls `POST /api/v1/simulation`.
- **Acceptance Criteria:**
  - Displays buffer violation status (`[ BUFFER VIOLATION ]` vs `[ BUFFER PRESERVED ]`).
- **Verification Commands:** `cd frontend/web && npm run build`

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
- **Objective:** Implement abstract base class `LLMProvider` and concrete client `LlamaCppProvider` communicating natively with local `llama.cpp` HTTP server (`http://localhost:8080/completion`).
- **Detailed Specifications:**
  1. `LLMProvider` abstract method: `def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str`.
  2. `LlamaCppProvider` constructor: `def __init__(self, endpoint: str = "http://localhost:8080/completion", timeout_seconds: float = 30.0)`.
  3. Formats prompt with Qwen ChatML tokens: `<|im_start|>system\n...<|im_end|>\n<|im_start|>user\n...<|im_end|>\n<|im_start|>assistant\n`.
  4. Manages connection pooling, HTTP status verification, and fallback triggers.
- **Acceptance Criteria:**
  - Successfully communicates with llama.cpp server and returns generated text.
  - Zero emojis in prompts or code.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_agent_tools.py`

---

### Task SC-002: Implement Deterministic `MockLLMProvider` for Testing & CI
- **Ticket ID:** `SC-002`
- **Workstream:** Agentic AI Layer
- **Owner:** The Scribe
- **Priority:** P0
- **Target Files:**
  - `backend/agent/llm_provider.py`
- **Objective:** Implement `MockLLMProvider` returning reproducible, schema-compliant `AgentResponse` JSON fixtures for offline execution and automated test validation.
- **Detailed Specifications:**
  1. Returns pre-computed JSON containing `recommendation`, `reason`, `evidence`, `confidence`, `alternatives`, and `competing_objectives_considered`.
  2. Validates against `AgentResponse` Pydantic model.
- **Acceptance Criteria:**
  - Unit tests run in under 0.05 seconds with 100% deterministic output.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_agent_tools.py`

---

### Task SC-003: Implement Deterministic Agent Evidence Assembly Tools
- **Ticket ID:** `SC-003`
- **Workstream:** Agentic AI Layer
- **Owner:** The Scribe
- **Priority:** P0
- **Target Files:**
  - `backend/agent/tools.py`
- **Objective:** Implement deterministic tool functions that extract factual evidence metrics from `FinancialState` to ground LLM reasoning.
- **Detailed Specifications:**
  1. `AgentTools.gather_evidence_for_liquidity(state: FinancialState) -> List[Evidence]`:
     - Compiles `current_balance`, `projected_balance`, `minimum_cash_buffer`, and `upcoming_obligations`.
     - Assigns `UncertaintyStatus` (`CONFIRMED`, `ESTIMATED`, `UNCERTAIN`).
  2. `AgentTools.run_balance_forecast(state: FinancialState) -> Dict[str, Any]`.
  3. `AgentTools.detect_signals(state: FinancialState) -> Dict[str, Any]`.
- **Acceptance Criteria:**
  - Never performs loose floating-point math inside the agent; extracts verified engine metrics.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_agent_tools.py`

---

### Task SC-004: Implement Evidence-Grounded Prompt Synthesis Engine
- **Ticket ID:** `SC-004`
- **Workstream:** Agentic AI Layer
- **Owner:** The Scribe
- **Priority:** P0
- **Target Files:**
  - `backend/agent/graph.py`
- **Objective:** Build prompt formatting logic grounding Qwen reasoning in exact numerical facts and enforcing Pydantic schema generation.
- **Detailed Specifications:**
  1. System prompt defines objective financial advisor persona, requiring schema compliance and tradeoff resolution.
  2. User prompt dynamically injects:
     - User balance, forecast, obligations, and buffer.
     - Formatted evidence metrics list.
     - Specific user query or event trigger.
- **Acceptance Criteria:**
  - Prompts contain zero emojis.
  - Instructions explicitly prohibit mathematical fabrication.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_agent_tools.py`

---

### Task SC-005: Build LangGraph Workflow with Self-Correction & Fallback
- **Ticket ID:** `SC-005`
- **Workstream:** Agentic AI Layer
- **Owner:** The Scribe
- **Priority:** P0
- **Target Files:**
  - `backend/agent/graph.py`
- **Objective:** Implement the `FinancialReasoningAgent` class managing state retrieval, tool execution, LLM synthesis, schema validation, and deterministic fallback generation.
- **Detailed Specifications:**
  1. `run(self, request: AgentRequest, state: FinancialState) -> AgentResponse`:
     - Step 1: Call `AgentTools.gather_evidence_for_liquidity(state)`.
     - Step 2: Invoke `llm_provider.generate()`.
     - Step 3: Parse and validate JSON against `AgentResponse`.
     - Step 4: If parsing fails, trigger `_deterministic_fallback(user_id, state, evidence)`.
  2. `_deterministic_fallback`: Synthesizes exact rule-based recommendation adhering to `AgentResponse` contract.
- **Acceptance Criteria:**
  - Guarantees valid `AgentResponse` return under all failure conditions.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_agent_tools.py`

---

### Task SC-006: Implement Multi-Objective Tradeoff Reasoning
- **Ticket ID:** `SC-006`
- **Workstream:** Agentic AI Layer
- **Owner:** The Scribe
- **Priority:** P1
- **Target Files:**
  - `backend/agent/graph.py`
- **Objective:** Implement prompt instructions and logic to explicitly evaluate competing financial objectives (e.g. liquidity preservation vs investment compounding vs vacation goal).
- **Detailed Specifications:**
  1. Populates `competing_objectives_considered` with structured explanations.
  2. Generates at least two distinct `alternatives` for user choice.
- **Acceptance Criteria:**
  - Output contains clear tradeoff rationales and alternative options.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_agent_tools.py`

---

## 3. The Alchemist (Financial Engine & Ingestion)

### Task AL-001: Implement Indian Banking SMS Regex Parser
- **Ticket ID:** `AL-001`
- **Workstream:** Ingestion and Normalization
- **Owner:** The Alchemist
- **Priority:** P0
- **Target Files:**
  - `backend/ingestion/sms_parser.py`
  - `backend/ingestion/__init__.py`
- **Objective:** Implement `SMSParser.parse_sms(raw_text, user_id, default_account_id)` with robust regex patterns for Indian banking institutions (HDFC, ICICI, SBI, Axis).
- **Detailed Specifications:**
  1. Extract:
     - Monetary amount (e.g. `INR 12,000.00` -> `12000.0`).
     - Transaction type (`DEBIT` vs `CREDIT`).
     - Account number reference (e.g. `XX4102`).
     - Merchant/Payee description (e.g. `Care Diagnostics`).
  2. Categorization heuristic:
     - Keywords `hospital`, `medical`, `diagnostics`, `clinic` -> `TransactionCategory.UNEXPECTED`.
     - Keywords `salary`, `payroll` -> `TransactionCategory.INCOME`.
     - Keywords `supermarket`, `groceries` -> `TransactionCategory.GROCERIES`.
  3. Calculate confidence score $[0.5, 1.0]$ based on captured fields.
- **Acceptance Criteria:**
  - Parses demo emergency SMS with amount `12000.0` and confidence $\ge 0.8$.
  - Does not fabricate missing fields.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_normalizer.py`

---

### Task AL-002: Implement Financial Event Normalizer
- **Ticket ID:** `AL-002`
- **Workstream:** Ingestion and Normalization
- **Owner:** The Alchemist
- **Priority:** P0
- **Target Files:**
  - `backend/ingestion/normalizer.py`
- **Objective:** Implement `FinancialEventNormalizer` converting raw SMS strings and raw transaction dictionaries into canonical `FinancialEvent` and `Transaction` instances.
- **Detailed Specifications:**
  1. `normalize_sms(user_id, raw_sms, event_id=None) -> FinancialEvent`.
  2. `normalize_transaction_dict(user_id, data, event_id=None) -> FinancialEvent`.
  3. Attaches provenance metadata: `source="sms"`, `timestamp`, and `confidence`.
- **Acceptance Criteria:**
  - Normalizes input into validated Pydantic model.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_normalizer.py`

---

### Task AL-003: Implement Deterministic `FinancialStateCalculator`
- **Ticket ID:** `AL-003`
- **Workstream:** Financial Engine
- **Owner:** The Alchemist
- **Priority:** P0
- **Target Files:**
  - `backend/financial_engine/state_calculator.py`
  - `backend/financial_engine/__init__.py`
- **Objective:** Implement `FinancialStateCalculator.calculate_state(...)` computing the canonical mathematical state.
- **Detailed Specifications:**
  1. Liquid Available Cash: `current_balance - immediate_bills_due_within_7_days`.
  2. Fixed / Variable / Discretionary expenses aggregation from recent transactions.
  3. Emergency fund coverage (months): `liquid_savings / monthly_fixed_expenses`.
  4. Savings rate: `(monthly_income - total_monthly_expenses) / monthly_income`.
  5. Projected cycle-end balance: `current_balance - upcoming_obligations - remaining_variable_burn`.
  6. Data completeness score: fraction of 5 core dimensions populated.
- **Acceptance Criteria:**
  - Recomputes state deterministically with zero floating-point drift.
  - Matches demo scenario metrics (Current Balance: 30,000; Available Cash: 12,000; Projected: 19,400).
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_financial_engine.py`

---

### Task AL-004: Implement 30-Day Trajectory Forecaster (`BalanceForecaster`)
- **Ticket ID:** `AL-004`
- **Workstream:** Financial Engine
- **Owner:** The Alchemist
- **Priority:** P0
- **Target Files:**
  - `backend/financial_engine/forecasting.py`
- **Objective:** Implement `BalanceForecaster.forecast_30_days(state, scheduled_bills, daily_discretionary_burn) -> Forecast`.
- **Detailed Specifications:**
  1. Computes daily trajectory points $t \in [0, 29]$:
     - Deducts daily variable burn.
     - Deducts scheduled bills due on day $t$.
     - Credits monthly income on scheduled paydays (e.g. day 1).
     - Identifies buffer violations (`is_below_buffer = running_balance < minimum_cash_buffer`).
  2. Calculates `minimum_projected_balance` and `lowest_balance_date`.
- **Acceptance Criteria:**
  - Generates 30 projection points and identifies lowest cash day.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_financial_engine.py`

---

### Task AL-005: Implement Deterministic Risk Detection Engine (`RiskDetector`)
- **Ticket ID:** `AL-005`
- **Workstream:** Financial Engine
- **Owner:** The Alchemist
- **Priority:** P0
- **Target Files:**
  - `backend/financial_engine/risk_detector.py`
- **Objective:** Implement `RiskDetector.detect_risks(state: FinancialState) -> List[RiskSignal]`.
- **Detailed Specifications:**
  1. Liquidity Deficit:
     - Trigger: `state.projected_balance < state.minimum_cash_buffer`.
     - Severity: `CRITICAL` if balance $\le 0$, else `MEDIUM`.
     - Impact: `state.minimum_cash_buffer - state.projected_balance` (e.g. INR 5,600).
  2. Upcoming Obligation Gap:
     - Trigger: `state.available_cash < state.upcoming_obligations`.
  3. Emergency Fund Depletion:
     - Trigger: `state.emergency_fund_months < 1.0`.
- **Acceptance Criteria:**
  - Emits `RiskSignal(type="liquidity", severity="medium", amount_impact=5600.0)` on demo data.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_financial_engine.py`

---

### Task AL-006: Implement Opportunity Detection Engine (`OpportunityDetector`)
- **Ticket ID:** `AL-006`
- **Workstream:** Financial Engine
- **Owner:** The Alchemist
- **Priority:** P1
- **Target Files:**
  - `backend/financial_engine/risk_detector.py`
- **Objective:** Implement `OpportunityDetector.detect_opportunities(state: FinancialState) -> List[OpportunitySignal]`.
- **Detailed Specifications:**
  1. Discretionary Spend Cushion:
     - Trigger: `state.discretionary_expenses > 4000`.
     - Benefit: $45\%$ of discretionary spending (e.g. INR 4,000).
  2. Surplus Allocation:
     - Trigger: `state.projected_balance > state.minimum_cash_buffer + 15000`.
- **Acceptance Criteria:**
  - Detects expense reduction opportunity deterministically.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_financial_engine.py`

---

### Task AL-007: Implement What-If Simulation Mathematical Engine
- **Ticket ID:** `AL-007`
- **Workstream:** Financial Engine
- **Owner:** The Alchemist
- **Priority:** P1
- **Target Files:**
  - `backend/services/orchestrator.py`
- **Objective:** Implement deterministic trajectory delta calculation for simulated cash flow shocks.
- **Detailed Specifications:**
  1. `run_simulation(sim_req: SimulationRequest) -> SimulationResult`.
  2. Calculates `baseline_projected_balance`, `simulated_projected_balance`, `buffer_violation_risk`, and goal delay impacts.
- **Acceptance Criteria:**
  - Returns exact numerical simulation results conforming to Pydantic contract.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_api.py`

---

## 4. King's Hand (Backend, API, Integration & Deployment)

### Task KH-001: Setup FastAPI Application & Centralized Pydantic Validation
- **Ticket ID:** `KH-001`
- **Workstream:** Backend Integration
- **Owner:** King's Hand
- **Priority:** P0
- **Target Files:**
  - `backend/main.py`
  - `backend/api/routes.py`
  - `backend/requirements.txt`
- **Objective:** Initialize FastAPI application with CORS middleware, global exception handlers returning `APIError` contracts, and healthcheck route.
- **Detailed Specifications:**
  1. Route `GET /api/v1/health` -> `{"status": "healthy"}`.
  2. Route `GET /` -> system status and docs URL.
  3. Custom exception handler formatting unhandled errors into `APIError(error_code="INTERNAL_SERVER_ERROR", message=...)`.
- **Acceptance Criteria:**
  - Server runs cleanly on `0.0.0.0:8000`.
  - Swagger UI accessible at `/docs`.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_api.py`

---

### Task KH-002: Implement Ingestion API Endpoints
- **Ticket ID:** `KH-002`
- **Workstream:** Backend Integration
- **Owner:** King's Hand
- **Priority:** P0
- **Target Files:**
  - `backend/api/routes.py`
- **Objective:** Implement validated ingestion endpoints accepting transactions and normalized events.
- **Detailed Specifications:**
  1. `POST /api/v1/transactions`:
     - Body: `Transaction`.
     - Calls `orchestrator.process_transaction(transaction)`.
     - Returns: `Transaction`.
  2. `POST /api/v1/financial-events`:
     - Body: `FinancialEvent`.
     - Calls `orchestrator.process_incoming_event(event)`.
     - Returns: `FinancialEvent`.
- **Acceptance Criteria:**
  - Rejects invalid schemas with HTTP 422.
  - Updates repository state on valid ingestion.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_api.py`

---

### Task KH-003: Implement State, Dashboard & Simulation Endpoints
- **Ticket ID:** `KH-003`
- **Workstream:** Backend Integration
- **Owner:** King's Hand
- **Priority:** P0
- **Target Files:**
  - `backend/api/routes.py`
- **Objective:** Implement financial state retrieval, aggregated dashboard, and simulation endpoints.
- **Detailed Specifications:**
  1. `GET /api/v1/financial-state?user_id=...` -> `FinancialState`.
  2. `GET /api/v1/dashboard?user_id=...` -> `DashboardResponse`.
  3. `POST /api/v1/simulation` -> `SimulationResult`.
  4. `POST /api/v1/agent/analyze` -> `AgentResponse`.
- **Acceptance Criteria:**
  - All endpoints validate inputs and responses with Pydantic schemas.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_api.py`

---

### Task KH-004: Build InMemory & Seeded Financial Repository
- **Ticket ID:** `KH-004`
- **Workstream:** Backend Integration
- **Owner:** King's Hand
- **Priority:** P0
- **Target Files:**
  - `backend/repositories/financial_repository.py`
- **Objective:** Implement `InMemoryFinancialRepository` pre-seeded with the primary demo user dataset (INR 42k starting balance, INR 65k salary, INR 18k bills, INR 25k buffer).
- **Detailed Specifications:**
  1. Methods: `get_balance()`, `set_balance()`, `get_transactions()`, `add_transaction()`, `get_income_records()`, `get_bills()`, `get_goals()`, `get_preferences()`.
  2. Global singleton `repo` instance.
- **Acceptance Criteria:**
  - Provides thread-safe, fast state access for API and agent.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_financial_engine.py`

---

### Task KH-005: Build Golden Path Service Orchestrator
- **Ticket ID:** `KH-005`
- **Workstream:** Backend Integration
- **Owner:** King's Hand
- **Priority:** P0
- **Target Files:**
  - `backend/services/orchestrator.py`
  - `backend/tests/test_golden_path.py`
- **Objective:** Implement `FinancialOrchestrator` integrating Ingestion -> Engine -> State -> Risk -> Agent -> Output into a unified pipeline.
- **Detailed Specifications:**
  1. `process_incoming_event(event: FinancialEvent)`:
     - Updates repository with transaction/event.
     - Recalculates `FinancialState` and detects risks.
     - Invokes `FinancialReasoningAgent.run()`.
     - Returns dictionary containing `event`, `financial_state`, and `agent_response`.
  2. `get_dashboard(user_id: str) -> DashboardResponse`.
- **Acceptance Criteria:**
  - Golden path integration test passes end-to-end.
- **Verification Commands:** `source .venv_system/bin/activate && PYTHONPATH=. pytest backend/tests/test_golden_path.py`

---

### Task KH-006: Setup Native AWS EC2 Deployment Systemd Units
- **Ticket ID:** `KH-006`
- **Workstream:** Backend Integration / DevOps
- **Owner:** King's Hand
- **Priority:** P1
- **Target Files:**
  - `deployment/aws/fastapi.service`
  - `deployment/aws/llamacpp.service`
  - `deployment/aws/nginx.conf`
  - `deployment/aws/setup_ec2.sh`
- **Objective:** Provide automated provisioning scripts and systemd service units for native execution on Ubuntu 22.04 / 24.04 LTS EC2 instances without Docker.
- **Detailed Specifications:**
  1. `setup_ec2.sh`: Clones repo, creates Python venv, installs dependencies, compiles native llama.cpp.
  2. `llamacpp.service`: Runs `llama-server` on port 8080.
  3. `fastapi.service`: Runs `uvicorn backend.main:app` on port 8000.
  4. `nginx.conf`: Reverse proxy mapping port 80/443 to port 8000.
- **Acceptance Criteria:**
  - Zero Docker or Kubernetes files.
- **Verification Commands:** `bash -n deployment/aws/setup_ec2.sh`
