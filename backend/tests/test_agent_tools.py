import json
import re
import pytest
from shared.contracts.contracts import AgentRequest, FinancialState, UserPreferences
from backend.agent.llm_provider import LLMProvider, LlamaCppProvider, MockLLMProvider
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

    assert response.user_id == "user_demo_01"
    assert response.recommendation is not None
    assert response.confidence >= 0.8
    assert len(response.evidence) > 0
    assert len(response.alternatives) > 0


def test_zero_emojis_in_llm_provider_code():
    provider = MockLLMProvider()
    out = provider.generate("Test prompt")
    emoji_pattern = re.compile(
        "[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\U0001f300-\U0001f5ff\U0001f600-\U0001f64f\U0001f680-\U0001f6ff]"
    )
    assert not emoji_pattern.search(out)

