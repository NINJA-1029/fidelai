import time
from datetime import datetime, timezone
from backend.ingestion.normalizer import FinancialEventNormalizer
from backend.services.orchestrator import orchestrator
from shared.contracts.contracts import (
    RiskType,
    SimulationRequest,
    TransactionType,
    UncertaintyStatus,
)


def test_complete_golden_path_pipeline():
    """
    Validates the Golden Path end-to-end:
    SMS Input -> Normalization -> FinancialEvent -> State Recalculation ->
    Risk Signal Detection -> Agent Reasoning -> Evidence-Backed Recommendation.
    """
    user_id = "user_demo_01"
    start_time = time.perf_counter()

    # 1. Ingest raw banking SMS for unexpected medical debit
    raw_sms = "INR 12,000.00 debited from A/C XX4102 on 28-Aug-2026 at Care Diagnostics. Avl Bal: INR 30,000.00"

    # 2. Normalize SMS into FinancialEvent
    event = FinancialEventNormalizer.normalize_sms(user_id=user_id, raw_sms=raw_sms)
    assert event.event_type == "transaction_created"
    assert event.transaction is not None
    assert event.transaction.amount == 12000.0
    assert event.transaction.type == TransactionType.DEBIT
    assert event.payload["available_balance"] == 30000.0

    # 3. Process via Orchestrator
    result = orchestrator.process_incoming_event(event)

    # 4. Verify Performance Criterion (< 2.0 seconds)
    total_duration = time.perf_counter() - start_time
    assert total_duration < 2.0, f"Golden path took {total_duration:.3f}s (must be < 2.0s)"
    assert "execution_time_ms" in result

    # 5. Verify updated Financial State
    state = result["financial_state"]
    assert state.user_id == user_id
    assert state.current_balance == 30000.0
    assert state.projected_balance < state.minimum_cash_buffer  # 8350 < 25000 (Safety buffer breached)

    # 6. Verify Deterministic Risk Detection
    assert len(state.risk_signals) > 0
    assert any(r.type == RiskType.LIQUIDITY for r in state.risk_signals)
    assert any(r.type == RiskType.UPCOMING_OBLIGATION for r in state.risk_signals)

    # 7. Verify Agent Reasoning & Explainable Decision Support
    agent_response = result["agent_response"]
    assert agent_response.user_id == user_id
    assert agent_response.recommendation is not None
    assert agent_response.recommendation.priority in ["high", "critical"]
    assert "liquidity" in agent_response.recommendation.category.lower()
    assert agent_response.confidence >= 0.85

    # 8. Verify Deterministic Evidence Grounding
    assert len(agent_response.evidence) >= 3
    evidence_metrics = [e.metric for e in agent_response.evidence]
    assert "projected_balance" in evidence_metrics
    assert "minimum_cash_buffer" in evidence_metrics
    for ev in agent_response.evidence:
        assert isinstance(ev.status, UncertaintyStatus)
        assert ev.value is not None

    # 9. Verify Alternatives and Tradeoffs Evaluated
    assert len(agent_response.alternatives) >= 2
    assert len(agent_response.competing_objectives_considered) >= 1


def test_golden_path_simulation_and_dashboard_integration():
    """
    Validates simulation engine and unified dashboard assembly downstream from orchestrator state.
    """
    user_id = "user_demo_01"

    # 1. Run What-If Simulation
    sim_request = SimulationRequest(
        user_id=user_id,
        scenario_type="unexpected_expense",
        amount=15000.0,
        description="Car Engine Repair"
    )
    sim_result = orchestrator.run_simulation(sim_request)
    assert sim_result.user_id == user_id
    assert sim_result.buffer_violation_risk is True
    assert sim_result.simulated_projected_balance < sim_result.baseline_projected_balance
    assert len(sim_result.goal_impacts) > 0

    # 2. Assemble Full Dashboard
    dashboard = orchestrator.get_dashboard(user_id)
    assert dashboard.user_id == user_id
    assert dashboard.financial_state is not None
    assert dashboard.forecast_30_days is not None
    assert len(dashboard.forecast_30_days.projection_points) == 30
    assert len(dashboard.recent_transactions) > 0


def test_golden_path_heterogeneous_batch_ingestion():
    """
    Validates batch normalization and sequential processing of multi-channel financial feeds.
    """
    user_id = "user_demo_01"

    items = [
        {
            "source": "receipt",
            "merchant_name": "Apollo Pharmacy",
            "total_amount": 1500.0,
            "category": "healthcare",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "source": "manual",
            "amount": 350.0,
            "type": "debit",
            "category": "dining",
            "description": "Coffee with colleague"
        }
    ]

    events = FinancialEventNormalizer.normalize_batch(user_id, items)
    assert len(events) == 2

    result = orchestrator.process_batch_events(user_id, events)
    assert result["financial_state"].user_id == user_id
    assert result["agent_response"] is not None
