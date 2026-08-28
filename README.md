# Agentic AI Financial Management System

## 1. Project Overview

The Agentic AI Financial Management System continuously transforms fragmented, heterogeneous financial information into an evolving canonical model of a user's financial state.

The system deterministically detects proactive risks and opportunities, simulates what-if scenarios, and provides explainable, evidence-backed decision support via a local LLM reasoning engine (Qwen 3.8 27B GGUF running natively on llama.cpp).

### The Golden Path
```
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
```

---

## 2. Core Operational Rules

1. Absolute Emoji Prohibition: Zero emojis anywhere in the repository (code, comments, docs, commits, logs, UI).
2. Absolute Container Prohibition: No Docker, no Kubernetes, no container registries. All services run natively on host OS / EC2 Ubuntu.
3. Deterministic Arithmetic: The LLM is never the calculator. All financial calculations are computed deterministically by the Financial Engine.
4. Contract-First and Mock-First: Development is coordinated via shared Pydantic models in `shared/contracts/` and mock fixtures in `shared/fixtures/`.

---

## 3. Developer Ownership and Directory Boundaries

There are four dedicated developer roles for the 24-hour sprint:

### Dev 1: High Warden (Flutter + UI)
- Directory: `frontend/`
- Responsibilities: Mobile application, Riverpod state management, GoRouter, zero-radius design system (0px container radius, 75px full pill buttons/badges), Lucide icons, screen layouts, API client integration.

### Dev 2: The Scribe (AI / Agentic Workflow)
- Directory: `backend/agent/`
- Responsibilities: LangGraph state machine, `LLMProvider` abstraction, local `llama.cpp` integration, deterministic tool execution, factual evidence synthesis, tradeoff reasoning, `AgentResponse` validation.

### Dev 3: The Alchemist (Financial Engine + Datasets)
- Directories: `backend/financial_engine/`, `backend/ingestion/`, `shared/fixtures/`
- Responsibilities: Ingestion normalizers (SMS, receipts, CSV), canonical `FinancialState` calculation, 30-day balance forecasting, deterministic risk/opportunity detection, uncertainty metrics, demo dataset scenarios.

### Dev 4: King's Hand (Backend + AWS + Integration)
- Directories: `backend/api/`, `backend/models/`, `backend/repositories/`, `backend/services/`, `deployment/`
- Responsibilities: FastAPI application, Pydantic schemas, PostgreSQL/Supabase database models, repository layer, endpoint orchestration, end-to-end integration, native AWS EC2 deployment automation, CI/CD, final merge authority.

---

## 4. Repository Structure

```
/
├── .agents/
│   └── skills/
│       └── start-task/
│           └── SKILL.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── feature_task.md
│   │   └── bug_report.md
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── agent/                 # LangGraph, LLMProvider, Tools (The Scribe)
│   ├── api/                   # FastAPI routes (King's Hand)
│   ├── financial_engine/      # Deterministic math & forecasting (The Alchemist)
│   ├── ingestion/             # SMS and transaction normalizers (The Alchemist)
│   ├── models/                # SQLAlchemy database models (King's Hand)
│   ├── repositories/          # Persistence layer (King's Hand)
│   ├── services/              # Orchestration (King's Hand)
│   ├── tests/                 # Backend unit & integration test suites
│   ├── main.py                # FastAPI entrypoint
│   └── requirements.txt       # Python dependencies
├── frontend/
│   └── flutter_app/           # Flutter mobile client (High Warden)
├── shared/
│   ├── contracts/             # Canonical Pydantic schemas
│   └── fixtures/              # Mock JSON testbeds (transactions, state, etc.)
├── docs/
│   ├── architecture.md        # Complete system blueprint
│   ├── contracts.md           # Schema & API specifications
│   ├── financial-state.md     # Mathematical formulations & risk triggers
│   ├── agent-design.md        # Agentic reasoning & LangGraph design
│   ├── ingestion.md           # Normalization & extraction rules
│   ├── deployment.md          # Native AWS EC2 deployment guide
│   ├── workflow.md            # Git & team operating protocol
│   └── issues_catalog.md      # P0, P1, P2 task backlog
├── AGENTS.md                  # Operational protocol & boundary definitions
├── README.md                  # System documentation
└── .env.example               # Environment variables template
```

---

## 5. Local Setup and Execution

### Prerequisites
- Python 3.10+
- Flutter 3.19+
- Git

### 1. Environment Setup
```bash
cp .env.example .env
```

### 2. Backend Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Run FastAPI Backend:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
Swagger API Documentation: `http://localhost:8000/docs`

### 3. Native llama.cpp LLM Server (Local Execution)
```bash
# In separate directory:
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp && make -j
./llama-server -m /path/to/qwen-3.8-27b.gguf --port 8080 -c 4096
```
*(Configure `LLM_PROVIDER=llamacpp` in `.env` to route live inferences to the local server).*


### 4. Frontend Setup
```bash
cd frontend/flutter_app
flutter pub get
flutter run
```

---

## 6. Running Tests

Execute backend test suite:
```bash
pytest backend/tests/ -v
```

Tests verify:
- Ingestion & SMS Regex Normalization (`test_normalizer.py`)
- FinancialState Math, 30-Day Trajectory & Risk Triggers (`test_financial_engine.py`)
- Agent Tools & Decision Reasoning (`test_agent_tools.py`)
- FastAPI Endpoints (`test_api.py`)
- Complete Golden Path Pipeline (`test_golden_path.py`)

---

## 7. Primary End-to-End Demo Scenario

- Baseline Financial State:
  - Bank Balance: INR 42,000.00
  - Monthly Expected Income: INR 65,000.00
  - Upcoming Obligation: INR 18,000.00
  - Emergency Fund: 2.1 months
  - Preferred Minimum Buffer: INR 25,000.00
  - Active Vacation Goal: INR 8,333.00/month
- Event Trigger:
  - Unexpected medical expense debit of INR 12,000.00 parsed from SMS.
- Deterministic Engine Calculation:
  - New Bank Balance: INR 30,000.00
  - Available Cash After Bills: INR 12,000.00
  - 30-Day Projected Month-End Balance: INR 19,400.00
  - Buffer Deficit: INR 5,600.00 below INR 25,000.00 safety threshold.
  - Active Risk Emitted: `RiskType.LIQUIDITY` (Severity: `MEDIUM`).
- Agentic AI Reasoning:
  - Evaluates tradeoffs: Protect liquid buffer vs delay vacation goal contribution vs preserve long-term investments.
  - Recommendation: "Preserve Near-Term Liquidity" by pausing vacation savings for 30 days and reducing discretionary dining by INR 4,000.00.
  - Output Delivered: Returned to Flutter with exact evidence metrics, confidence (0.94), and actionable alternative options.
