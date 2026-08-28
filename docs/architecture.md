# System Architecture

## 1. System Overview

The Agentic AI Financial Management System continuously ingests heterogeneous financial data, extracts structured facts, updates an authoritative financial state model, executes deterministic analytics (risk/opportunity/forecast/goals), and orchestrates an AI reasoning agent (LangGraph + Qwen 3.8 27B GGUF on native llama.cpp) to produce explainable, evidence-backed decision support.


```
                         FLUTTER MOBILE APP
                                |
                                | HTTPS / JSON (Pydantic / Freezed)
                                v
                           FASTAPI LAYER
                                |
              +-----------------+-----------------+
              |                 |                 |
              v                 v                 v
        POSTGRESQL /        FINANCIAL          AGENT LAYER
          SUPABASE            ENGINE                |
              |                 |                   v
              |                 v               LANGGRAPH
              |          FINANCIAL STATE            |
              |                 |                   v
              |                 |            DETERMINISTIC TOOLS
              |                 |                   |
              |                 +---------->        v
              |                                 llama.cpp
              |                                     |
              |                                     v
              |                                 QWEN GGUF
              |                                     |
              +-----------------+-------------------+
                                |
                                v
                     STRUCTURED RECOMMENDATION
                                |
                                v
                         FLUTTER UI
```

---

## 2. Component Boundaries and Separation of Concerns

### Ingestion Layer (`backend/ingestion/`)
- Ingests SMS strings, OCR receipt items, bank CSV feeds, and manual transaction inputs.
- Normalizes disparate schemas into `FinancialEvent` and `Transaction` models.
- Attaches provenance metadata: `source`, `confidence`, and `timestamp`.
- Strict Rule: Never fabricates missing data; flags uncertain data explicitly.

### Financial Engine (`backend/financial_engine/`)
- Sole mathematical authority of the system.
- Computes `FinancialState`, cash flow, 30-day forecast, savings pacing, liquidity buffers, and emergency fund status.
- Evaluates deterministic triggers for `RiskSignal` and `OpportunitySignal`.
- Strict Rule: Deterministic, repeatable, fast Python calculations using Pandas and NumPy.

### Agentic Reasoning Layer (`backend/agent/`)
- Implements LangGraph state machine workflow.
- Orchestrates deterministic tool calls to retrieve financial state facts and evidence metrics.
- Invokes Qwen via `LLMProvider` abstraction backed by native `llama.cpp`.
- Resolves competing financial goals (e.g., liquidity preservation vs investment return).
- Produces validated `AgentResponse` containing `Recommendation`, `reason`, `evidence`, and `confidence`.
- Strict Rule: LLM never computes math; it synthesizes facts and explains tradeoffs.

### Backend and Repository Layer (`backend/api/`, `backend/models/`, `backend/repositories/`)
- FastAPI endpoints for Flutter consumption and webhook ingestion.
- PostgreSQL/Supabase database schema with SQLAlchemy ORM and Alembic migrations.
- Structured Pydantic validation across all request/response boundaries.
- Native EC2 deployment via standard systemd service processes.

### Mobile Application (`frontend/flutter_app/`)
- Cross-platform Flutter application utilizing Riverpod for reactive state management.
- GoRouter for declarative routing across 7 primary screens.
- Zero-radius container aesthetic with 75px full pill action buttons and badges.
- Strict Rule: Pure presentation and contract consumer; zero business logic duplication.

---

## 3. The Golden Path Execution Flow

1. Input Ingestion: User sends SMS transaction or manual debit of INR 12,000.
2. Event Normalization: Ingestion normalizer parses string into `FinancialEvent` with `confidence: 0.98`.
3. State Recomputation: Financial Engine updates `FinancialState`, adjusting `current_balance` to INR 30,000.
4. Deterministic Analytics: Engine forecasts 30-day balance to INR 19,400, detecting a violation of the INR 25,000 minimum cash buffer.
5. Signal Emission: Engine creates `RiskSignal(type="liquidity", severity="medium", amount_impact=5600.0)`.
6. Agent Activation: LangGraph workflow receives trigger, queries deterministic financial tools, and compiles factual evidence.
7. Model Reasoning: Qwen evaluates competing priorities (liquidity preservation vs investment SIP vs vacation savings).
8. Recommendation Delivery: Structured JSON response returned via FastAPI to Flutter with clear metrics, rationale, and alternatives.

---

## 4. Absolute Infrastructure Mandates

- Native Host Execution: All processes (FastAPI, llama.cpp, Flutter tooling) run directly on host OS without containerization.
- No Docker: No Dockerfile, docker-compose, or container runtimes.
- No Kubernetes: No k8s manifests, Helm charts, or ingress controllers.
- Native AWS Deployment: AWS EC2 Ubuntu instance using Python venv, native llama.cpp binary, and systemd units.
