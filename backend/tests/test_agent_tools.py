import os
import json
import re
from typing import Optional
from datetime import datetime, timezone
import pytest


from shared.contracts.contracts import (
    AgentRequest,
    AgentResponse,
    FinancialState,
    FinancialGoal,
    UserPreferences,
    UncertaintyStatus,
)

from backend.agent.llm_provider import (
    LLMProvider,
    LlamaCppProvider,
    MockLLMProvider,
    get_llm_provider,
)
from backend.agent.tools import AgentTools
from backend.agent.graph import FinancialReasoningAgent


def test_llm_provider_abstract_interface():
    # Verify LLMProvider cannot be instantiated directly without implementing generate
    with pytest.raises(TypeError):
        LLMProvider()  # type: ignore


def test_llamacpp_provider_chatml_formatting():
    prompt = "Analyze recent liquidity movements."
    system_prompt = "You are a fiduciary AI financial advisor."
    formatted = LlamaCppProvider.format_chatml_prompt(prompt=prompt, system_prompt=system_prompt)

    assert "<|im_start|>system" in formatted
    assert system_prompt in formatted
    assert "<|im_end|>" in formatted
    assert "<|im_start|>user" in formatted
    assert prompt in formatted
    assert "<|im_start|>assistant\n" in formatted


def test_llamacpp_provider_initialization():
    provider = LlamaCppProvider(endpoint="http://localhost:8080/completion", timeout_seconds=45.0)
    assert provider.endpoint == "http://localhost:8080/completion"
    assert provider.timeout_seconds == 45.0
    provider.close()


def test_get_llm_provider_factory(monkeypatch):
    # 1. Explicit llamacpp
    p1 = get_llm_provider("llamacpp")
    assert isinstance(p1, LlamaCppProvider)
    p1.close()

    # 2. Explicit mock
    p2 = get_llm_provider("mock")
    assert isinstance(p2, MockLLMProvider)

    # 3. Environment resolution
    monkeypatch.setenv("LLM_PROVIDER", "llamacpp")
    monkeypatch.setenv("LLAMA_CPP_ENDPOINT", "http://127.0.0.1:9999/completion")
    p3 = get_llm_provider()
    assert isinstance(p3, LlamaCppProvider)
    assert p3.endpoint == "http://127.0.0.1:9999/completion"
    p3.close()

    # 4. Invalid provider must raise ValueError rather than silently falling back
    monkeypatch.setenv("LLM_PROVIDER", "invalid_cloud_provider")
    with pytest.raises(ValueError, match="Invalid or unsupported LLM_PROVIDER"):
        get_llm_provider()


def test_mock_llm_provider_default_generation():
    provider = MockLLMProvider()
    raw_output = provider.generate("Test prompt")
    assert isinstance(raw_output, str)


    parsed = json.loads(raw_output)
    assert "response_id" in parsed
    assert "recommendation" in parsed
    assert "evidence" in parsed
    assert "confidence" in parsed


def test_mock_llm_provider_canned_response():
    custom_canned = {
        "response_id": "resp_custom_001",
        "user_id": "user_demo_01",
        "recommendation": {
            "recommendation_id": "rec_custom_001",
            "title": "Custom Recommendation",
            "priority": "low",
            "description": "Custom test description.",
            "impact_amount": 1000.0,
            "category": "savings",
        },
        "reason": "Test custom reason.",
        "evidence": [],
        "confidence": 0.99,
        "alternatives": ["Custom alternative"],
        "competing_objectives_considered": ["Custom tradeoff"],
    }
    provider = MockLLMProvider(canned_response_dict=custom_canned)
    raw_output = provider.generate("Test prompt")
    parsed = json.loads(raw_output)
    assert parsed["response_id"] == "resp_custom_001"
    assert parsed["recommendation"]["title"] == "Custom Recommendation"


def test_mock_llm_provider_failure_modes():
    # 1. Complete failure
    failing_provider = MockLLMProvider(should_fail=True)
    with pytest.raises(RuntimeError, match="Simulated LLM server connection failure"):
        failing_provider.generate("Test prompt")

    # 2. Malformed JSON on first call, valid on second
    retry_provider = MockLLMProvider(fail_malformed_json_once=True)
    first_call = retry_provider.generate("Prompt 1")
    assert "MALFORMED_JSON" in first_call
    second_call = retry_provider.generate("Prompt 2")
    assert json.loads(second_call)["response_id"] == "resp_mock_001"


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
        minimum_cash_buffer=25000.0,
    )
    evidence = AgentTools.gather_evidence_for_liquidity(state)
    assert len(evidence) >= 4

    metrics = {e.metric: e.value for e in evidence}
    assert metrics["current_balance"] == 30000.0
    assert metrics["projected_balance"] == 19400.0
    assert metrics["minimum_cash_buffer"] == 25000.0

    statuses = {e.metric: e.status for e in evidence}
    assert statuses["current_balance"] == UncertaintyStatus.CONFIRMED
    assert statuses["projected_balance"] == UncertaintyStatus.ESTIMATED


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
        minimum_cash_buffer=25000.0,
    )
    agent = FinancialReasoningAgent(llm_provider=MockLLMProvider())
    req = AgentRequest(user_id="user_demo_01", user_query="What should I do about my balance deficit?")
    response = agent.run(req, state)

    assert isinstance(response, AgentResponse)
    assert response.user_id == "user_demo_01"
    assert response.recommendation is not None
    assert response.confidence >= 0.8
    assert len(response.evidence) > 0
    assert len(response.alternatives) > 0


def test_agent_self_correction_retry():
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
        minimum_cash_buffer=25000.0,
    )
    # Fails with malformed JSON on first attempt, corrects and succeeds on retry
    mock_provider = MockLLMProvider(fail_malformed_json_once=True)
    agent = FinancialReasoningAgent(llm_provider=mock_provider)
    req = AgentRequest(user_id="user_demo_01", user_query="Assess cash flow status")
    response = agent.run(req, state)

    assert isinstance(response, AgentResponse)
    assert response.user_id == "user_demo_01"
    assert mock_provider._calls_count == 2
    assert response.recommendation is not None


def test_agent_deterministic_fallback_on_failure():
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
        minimum_cash_buffer=25000.0,
    )
    failing_provider = MockLLMProvider(should_fail=True)
    agent = FinancialReasoningAgent(llm_provider=failing_provider)
    req = AgentRequest(user_id="user_demo_01", user_query="What to do?")
    response = agent.run(req, state)

    assert isinstance(response, AgentResponse)
    assert response.user_id == "user_demo_01"
    assert "resp_fallback_" in response.response_id
    assert response.recommendation.priority == "high"
    assert response.recommendation.impact_amount == 5600.0  # 25000 - 19400
    assert len(response.alternatives) >= 2


def test_agent_deterministic_fallback_surplus():
    state = FinancialState(
        user_id="user_demo_01",
        current_balance=45000.0,
        available_cash=27000.0,
        expected_monthly_income=65000.0,
        fixed_expenses=24000.0,
        variable_expenses=12000.0,
        discretionary_expenses=8500.0,
        recurring_obligations=24000.0,
        upcoming_obligations=18000.0,
        projected_balance=35000.0,
        minimum_cash_buffer=25000.0,
    )
    failing_provider = MockLLMProvider(should_fail=True)
    agent = FinancialReasoningAgent(llm_provider=failing_provider)
    req = AgentRequest(user_id="user_demo_01")
    response = agent.run(req, state)

    assert isinstance(response, AgentResponse)
    assert response.recommendation.title == "Deploy Surplus Liquidity"
    assert response.recommendation.priority == "medium"
    assert len(response.alternatives) >= 2


def test_langgraph_compiled_structure():
    agent = FinancialReasoningAgent(llm_provider=MockLLMProvider())
    assert hasattr(agent, "graph")
    assert agent.graph is not None

    # Inspect graph node keys
    nodes = agent.graph.nodes
    expected_nodes = {
        "__start__",
        "gather_evidence",
        "synthesize_prompt",
        "llm_inference",
        "validate_output",
        "self_correct_retry",
        "deterministic_fallback",
    }
    for expected in expected_nodes:
        assert expected in nodes, f"Expected node '{expected}' missing from compiled StateGraph"


def test_langgraph_retry_exhaustion_routes_to_fallback():
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
        minimum_cash_buffer=25000.0,
    )

    class AlwaysMalformedProvider(LLMProvider):
        def __init__(self):
            self.calls = 0

        def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
            self.calls += 1
            return "MALFORMED_OUTPUT_NEVER_JSON"

    provider = AlwaysMalformedProvider()
    agent = FinancialReasoningAgent(llm_provider=provider)
    req = AgentRequest(user_id="user_demo_01")
    response = agent.run(req, state)

    # Must make exactly 2 calls (initial + 1 bounded retry), then fallback
    assert provider.calls == 2
    assert isinstance(response, AgentResponse)
    assert "resp_fallback_" in response.response_id
    assert response.recommendation.title == "Preserve Near-Term Liquidity"


def test_llamacpp_provider_respects_max_tokens_and_temp(monkeypatch):
    monkeypatch.setenv("LLM_MAX_TOKENS", "2048")
    monkeypatch.setenv("LLM_TEMPERATURE", "0.25")
    provider = LlamaCppProvider()
    assert provider.max_tokens == 2048
    assert provider.temperature == 0.25
    provider.close()


def test_zero_emojis_in_reasoning_and_fallback():
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
        minimum_cash_buffer=25000.0,
    )
    # Test standard output
    agent = FinancialReasoningAgent(llm_provider=MockLLMProvider())
    req = AgentRequest(user_id="user_demo_01")
    res_normal = agent.run(req, state)

    # Test fallback output
    agent_fallback = FinancialReasoningAgent(llm_provider=MockLLMProvider(should_fail=True))
    res_fallback = agent_fallback.run(req, state)

    emoji_pattern = re.compile(
        "[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\U0001f300-\U0001f5ff\U0001f600-\U0001f64f\U0001f680-\U0001f6ff]"
    )

    for resp in [res_normal, res_fallback]:
        assert not emoji_pattern.search(resp.recommendation.title)
        assert not emoji_pattern.search(resp.recommendation.description)
        assert not emoji_pattern.search(resp.reason)
        for alt in resp.alternatives:
            assert not emoji_pattern.search(alt)
        for obj in resp.competing_objectives_considered:
            assert not emoji_pattern.search(obj)


def test_zero_emojis_in_llm_provider_code():
    provider = MockLLMProvider()
    out = provider.generate("Test prompt")
    emoji_pattern = re.compile(
        "[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\U0001f300-\U0001f5ff\U0001f600-\U0001f64f\U0001f680-\U0001f6ff]"
    )
    assert not emoji_pattern.search(out)


def test_agent_long_term_memory_persistence():
    from backend.repositories.financial_repository import repo
    user_id = "user_demo_01"
    state = FinancialState(
        user_id=user_id,
        current_balance=30000.0,
        available_cash=12000.0,
        expected_monthly_income=65000.0,
        fixed_expenses=24000.0,
        variable_expenses=12000.0,
        discretionary_expenses=8500.0,
        recurring_obligations=24000.0,
        upcoming_obligations=18000.0,
        projected_balance=19400.0,
        minimum_cash_buffer=25000.0,
    )
    agent = FinancialReasoningAgent(llm_provider=MockLLMProvider())

    # Run agent twice with different queries
    req1 = AgentRequest(user_id=user_id, user_query="Can I spend 5000 on shoes?")
    resp1 = agent.run(req1, state)
    assert resp1.user_id == user_id

    req2 = AgentRequest(user_id=user_id, user_query="What about next week?")
    resp2 = agent.run(req2, state)
    assert resp2.user_id == user_id

    # Verify memory history contains both runs in descending order
    memories = repo.get_agent_memories(user_id, limit=5)
    assert len(memories) >= 2
    assert memories[0].response_id == resp2.response_id

