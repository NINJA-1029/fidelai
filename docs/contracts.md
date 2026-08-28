# System Contracts and Schema Specification

## 1. Overview

To guarantee seamless parallel development among all four developers (High Warden, The Scribe, The Alchemist, King's Hand), every interface boundary is governed by immutable Pydantic schemas located in `shared/contracts/contracts.py`.

---

## 2. Core Entities

### Transaction
| Field | Type | Description |
|---|---|---|
| transaction_id | str | Unique identifier (e.g. `tx_001`) |
| user_id | str | User reference |
| account_id | str | Source bank/card account |
| amount | float | Non-negative transaction amount |
| currency | str | ISO 4217 code (default: `INR`) |
| type | str | `debit`, `credit`, `transfer` |
| category | str | `income`, `housing`, `utilities`, `groceries`, `unexpected`, etc. |
| description | str | Cleaned transaction description |
| timestamp | datetime | ISO 8601 UTC timestamp |
| source | str | `bank_api`, `sms`, `receipt`, `manual`, `csv` |
| confidence | float | Confidence score between 0.0 and 1.0 |
| is_recurring | bool | Recurring obligation flag |

### FinancialEvent
| Field | Type | Description |
|---|---|---|
| event_id | str | Unique event identifier |
| user_id | str | User reference |
| event_type | str | `transaction_created`, `bill_due`, `income_received`, `anomaly_detected` |
| timestamp | datetime | Event creation timestamp |
| source | str | Origin channel |
| confidence | float | Provenance reliability score |
| payload | dict | Contextual metadata |
| transaction | Transaction | Optional nested transaction entity |

### FinancialState
Authoritative mathematical snapshot of the user's financial posture:
| Field | Type | Description |
|---|---|---|
| user_id | str | User identifier |
| current_balance | float | Total liquid cash balance |
| available_cash | float | Balance minus immediate obligations |
| expected_monthly_income | float | Normalized monthly income |
| income_variability | float | Variance metric |
| income_confidence | float | Confidence in income timing/amount |
| fixed_expenses | float | Monthly committed fixed overhead |
| variable_expenses | float | Essential variable spending |
| discretionary_expenses | float | Discretionary lifestyle spending |
| recurring_obligations | float | Monthly recurring commitments |
| upcoming_obligations | float | Unpaid bills due within 30 days |
| savings | float | Liquid savings reserve |
| emergency_fund_months | float | Months of fixed expenses covered |
| savings_rate | float | Percentage of income saved |
| financial_goals | list[FinancialGoal] | Active goal progress list |
| investments_total_value | float | Total portfolio valuation |
| projected_balance | float | Deterministic 30-day projected balance |
| minimum_cash_buffer | float | User's preferred minimum buffer |
| risk_signals | list[RiskSignal] | Active risk signals |
| opportunity_signals | list[OpportunitySignal] | Active opportunity signals |
| data_completeness | float | Completeness ratio [0.0 - 1.0] |
| overall_confidence | float | Aggregate system confidence |

---

## 3. Agent and Decision Support Contracts

### AgentRequest
Payload passed to the LangGraph reasoning engine:
```json
{
  "user_id": "user_demo_01",
  "trigger_event": { ... },
  "user_query": "How will my medical bill affect my vacation goal?",
  "financial_state": null
}
```

### AgentResponse
Structured output returned by the Agent:
```json
{
  "response_id": "resp_001",
  "user_id": "user_demo_01",
  "recommendation": {
    "recommendation_id": "rec_001",
    "title": "Preserve Near-Term Liquidity",
    "priority": "high",
    "description": "Reduce discretionary spending by INR 4,000 to maintain your safety buffer.",
    "impact_amount": 4000.0,
    "category": "liquidity"
  },
  "reason": "An unexpected expense of INR 12,000 will compress month-end balance below INR 25,000.",
  "evidence": [
    {
      "metric": "projected_balance",
      "value": 19400.0,
      "threshold": 25000.0,
      "status": "estimated",
      "description": "Deterministic 30-day balance forecast"
    }
  ],
  "confidence": 0.94,
  "alternatives": [
    "Pause vacation goal contribution for 1 month",
    "Cut dining out budget"
  ],
  "competing_objectives_considered": [
    "Immediate cash safety vs secondary goal pacing"
  ],
  "generated_at": "2026-08-28T10:30:10Z"
}
```

---

## 4. API Endpoints Summary

| Method | Route | Request Contract | Response Contract | Description |
|---|---|---|---|---|
| GET | `/api/v1/health` | None | `{ "status": "healthy" }` | Healthcheck |
| POST | `/api/v1/transactions` | `Transaction` | `Transaction` | Ingest transaction |
| POST | `/api/v1/financial-events` | `FinancialEvent` | `FinancialEvent` | Ingest event |
| GET | `/api/v1/financial-state` | Query `user_id` | `FinancialState` | Fetch current state |
| POST | `/api/v1/agent/analyze` | `AgentRequest` | `AgentResponse` | Run AI reasoning |
| POST | `/api/v1/simulation` | `SimulationRequest` | `SimulationResult` | What-if simulation |
| GET | `/api/v1/dashboard` | Query `user_id` | `DashboardResponse` | Aggregated view |
