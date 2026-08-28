from shared.contracts.contracts import AgentRequest, FinancialState, UserPreferences
from backend.agent.graph import FinancialReasoningAgent
from backend.agent.llm_provider import MockLLMProvider
from backend.agent.tools import AgentTools


def test_agent_tools_evidence_gathering():
    state = FinancialState(
        user_id="user_demo_01",
        current_balance=30000.0,
        available_cash=12000.0,
        expected_monthly_income=65000.0,
        fixed_expenses=24000.0,
        variable_expenses=12000.0,
        discretionary_expenses=8500.0,
        recurring_obligations=24000.0,
        upcoming_obligations=18000.0,
        projected_balance=19400.0,
        minimum_cash_buffer=25000.0
    )
    evidence = AgentTools.gather_evidence_for_liquidity(state)
    assert len(evidence) >= 4
    
    metrics = {e.metric: e.value for e in evidence}
    assert metrics["current_balance"] == 30000.0
    assert metrics["projected_balance"] == 19400.0
    assert metrics["minimum_cash_buffer"] == 25000.0


def test_agent_reasoning_flow():
    state = FinancialState(
        user_id="user_demo_01",
        current_balance=30000.0,
        available_cash=12000.0,
        expected_monthly_income=65000.0,
        fixed_expenses=24000.0,
        variable_expenses=12000.0,
        discretionary_expenses=8500.0,
        recurring_obligations=24000.0,
        upcoming_obligations=18000.0,
        projected_balance=19400.0,
        minimum_cash_buffer=25000.0
    )
    agent = FinancialReasoningAgent(llm_provider=MockLLMProvider())
    req = AgentRequest(user_id="user_demo_01", user_query="What should I do about my balance deficit?")
    response = agent.run(req, state)

    assert response.user_id == "user_demo_01"
    assert response.recommendation is not None
    assert response.confidence >= 0.8
    assert len(response.evidence) > 0
    assert len(response.alternatives) > 0
