# Agentic AI Reasoning and LangGraph Architecture

## 1. Agent Mission and Design Philosophy

The Agentic Reasoning Layer (`backend/agent/`) acts as the cognitive synthesis engine of the system. It receives financial triggers and user queries, invokes deterministic tools to retrieve verified financial facts and evidence, and prompts a local Qwen 3.8 27B GGUF model via native `llama.cpp` to formulate explainable, contextual recommendations.


### Core Tenet
The LLM never computes financial arithmetic. The LLM evaluates trade-offs, synthesizes evidence, explains complex financial dynamics in accessible prose, and ranks alternative options based on user preferences.

---

## 2. LangGraph State Workflow

```
[START]
   |
   v
[Node: retrieve_state] (Fetches canonical FinancialState from repository/engine)
   |
   v
[Node: assess_triggers] (Evaluates active RiskSignals, OpportunitySignals, and user queries)
   |
   v
[Node: execute_tools] (Calls deterministic analytics tools to gather evidence)
   |
   v
[Node: resolve_competing_objectives] (Weights Liquidity vs Goals vs Investments based on UserPreferences)
   |
   v
[Node: synthesize_reasoning_llm] (Prompts Qwen with structured JSON context and evidence)
   |
   v
[Node: validate_and_format] (Validates Pydantic AgentResponse schema and confidence constraints)
   |
   v
 [END]
```

---

## 3. Deterministic Agent Tools

The Agent executes deterministic Python functions exposed as tools:

1. `calculate_financial_state(user_id)`: Recomputes and returns the full `FinancialState`.
2. `forecast_balance(user_id, horizon_days)`: Returns deterministic 30-day projection points and minimum balance date.
3. `check_upcoming_obligations(user_id, window_days)`: Returns pending unpaid bills due in the upcoming window.
4. `calculate_goal_progress(user_id)`: Computes deficit/surplus against target goal timelines.
5. `simulate_scenario(user_id, scenario_type, amount)`: Deterministically projects balance impact of an expense or income shock.

---

## 4. LLMProvider Abstraction

The agent does not depend on raw vendor SDKs. It depends on an abstract base class:

```python
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        pass
```

Implementations:
- `LlamaCppProvider`: Interacts directly with native `llama.cpp` server running locally on port 8080.
- `MockLLMProvider`: Deterministic mock provider returning structured fixtures for instant testing and CI/CD without requiring local GPU/GGUF weights.

---

## 5. Structured Prompt Architecture

Prompts are strictly grounded in deterministic evidence. An example prompt structure:

```text
SYSTEM:
You are an expert, objective financial intelligence engine.
Analyze the following structured financial state and evidence.
Synthesize an explainable, proactive recommendation.
Respect user preferences and resolve competing objectives.
You MUST output valid JSON conforming to the AgentResponse schema.

FACTS AND EVIDENCE:
- Current Liquid Balance: INR 30,000.00
- 30-Day Projected Balance: INR 19,400.00
- Preferred Minimum Cash Buffer: INR 25,000.00
- Upcoming Obligations (Next 14 Days): INR 18,000.00
- Recent Outflow: INR 12,000.00 (Emergency medical treatment)
- Active Goals: Emergency Fund (P1, on track), Vacation (P3, INR 8,333/mo)

TASK:
1. Identify primary risk and recommended mitigation.
2. Resolve competing priority between liquidity buffer and vacation goal.
3. Formulate 2 to 3 alternative actions.
```

---

## 6. Failure Handling and Fallback Strategy

If `LlamaCppProvider` encounters an unexpected error or if the generated JSON fails Pydantic schema validation:
1. Self-Correction Attempt: Retry prompt with schema validation error details once.
2. Deterministic Fallback: If retry fails, invoke deterministic rule-based template generation to guarantee that the user always receives a valid, schema-compliant `AgentResponse` backed by exact engine evidence.
