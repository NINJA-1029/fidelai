from backend.ingestion.normalizer import FinancialEventNormalizer
from backend.services.orchestrator import orchestrator
from shared.contracts.contracts import RiskType


def test_complete_golden_path_pipeline():
    """
    Validates the Golden Path:
    SMS Input -> Normalization -> FinancialEvent -> State Recalculation ->
    Risk Signal Detection -> Agent Reasoning -> Evidence-Backed Recommendation.
    """
    user_id = "user_demo_01"
    
    # 1. User receives unexpected medical expense SMS
    raw_sms = "INR 12,000.00 debited from A/C XX4102 on 28-Aug-2026 at Care Diagnostics. Avl Bal: INR 30,000.00"
    
    # 2. Normalize into FinancialEvent
    event = FinancialEventNormalizer.normalize_sms(user_id=user_id, raw_sms=raw_sms)
    assert event.event_type == "transaction_created"
    assert event.transaction is not None
    assert event.transaction.amount == 12000.0

    # 3. Process via Orchestrator
    result = orchestrator.process_incoming_event(event)
    
    # 4. Verify updated Financial State
    state = result["financial_state"]
    assert state.user_id == user_id
    assert state.current_balance == 30000.0
    
    # 5. Verify Risk Detection
    assert len(state.risk_signals) > 0
    assert any(r.type == RiskType.LIQUIDITY for r in state.risk_signals)
    
    # 6. Verify Agent Decision Support
    agent_response = result["agent_response"]
    assert agent_response.user_id == user_id
    assert agent_response.recommendation.priority == "high"
    assert "liquidity" in agent_response.recommendation.category.lower()
    assert agent_response.confidence >= 0.85
    assert len(agent_response.evidence) >= 3
    assert len(agent_response.alternatives) >= 2
