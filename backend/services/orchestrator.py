import logging
from typing import Optional, Dict, Any
from shared.contracts.contracts import (
    Transaction,
    FinancialEvent,
    FinancialState,
    AgentRequest,
    AgentResponse,
    DashboardResponse,
    SimulationRequest,
    SimulationResult,
)
from backend.repositories.financial_repository import repo
from backend.financial_engine.state_calculator import FinancialStateCalculator
from backend.financial_engine.forecasting import BalanceForecaster
from backend.financial_engine.risk_detector import RiskDetector, OpportunityDetector
from backend.agent.graph import FinancialReasoningAgent
from backend.agent.llm_provider import MockLLMProvider

logger = logging.getLogger(__name__)


class FinancialOrchestrator:
    """
    Central orchestration service executing the Golden Path pipeline.
    """

    def __init__(self, agent: Optional[FinancialReasoningAgent] = None):
        self.agent = agent or FinancialReasoningAgent(llm_provider=MockLLMProvider())

    def get_current_financial_state(self, user_id: str) -> FinancialState:
        balance = repo.get_balance(user_id)
        txns = repo.get_transactions(user_id)
        incomes = repo.get_income_records(user_id)
        bills = repo.get_bills(user_id)
        goals = repo.get_goals(user_id)
        preferences = repo.get_preferences(user_id)

        # 1. Deterministic state calculation
        state = FinancialStateCalculator.calculate_state(
            user_id=user_id,
            current_balance=balance,
            transactions=txns,
            income_records=incomes,
            bills=bills,
            goals=goals,
            preferences=preferences,
            investments_total_value=140000.0,
            liquid_savings=50000.0,
        )

        # 2. Attach detected signals
        state.risk_signals = RiskDetector.detect_risks(state)
        state.opportunity_signals = OpportunityDetector.detect_opportunities(state)

        return state

    def process_incoming_event(self, event: FinancialEvent) -> Dict[str, Any]:
        """
        Executes the full Golden Path: Ingestion -> State -> Risk -> Agent Reasoning -> Output.
        """
        user_id = event.user_id
        repo.add_event(user_id, event)

        if event.transaction:
            repo.add_transaction(user_id, event.transaction)

        # Recalculate financial state
        updated_state = self.get_current_financial_state(user_id)

        # Run AI Reasoning Agent
        agent_req = AgentRequest(user_id=user_id, trigger_event=event)
        agent_response = self.agent.run(agent_req, updated_state)

        return {
            "event": event,
            "financial_state": updated_state,
            "agent_response": agent_response
        }

    def process_transaction(self, txn: Transaction) -> Dict[str, Any]:
        event = FinancialEvent(
            event_id=f"evt_{txn.transaction_id}",
            user_id=txn.user_id,
            event_type="transaction_created",
            timestamp=txn.timestamp,
            source=txn.source,
            confidence=txn.confidence,
            payload=txn.model_dump(),
            transaction=txn
        )
        return self.process_incoming_event(event)

    def run_simulation(self, sim_req: SimulationRequest) -> SimulationResult:
        state = self.get_current_financial_state(sim_req.user_id)
        baseline_proj = state.projected_balance
        simulated_proj = baseline_proj - sim_req.amount
        violates_buffer = simulated_proj < state.minimum_cash_buffer
        deficit = max(0.0, state.minimum_cash_buffer - simulated_proj)

        impact_summary = (
            f"An immediate outflow of INR {sim_req.amount:,.2f} reduces projected month-end balance "
            f"from INR {baseline_proj:,.2f} to INR {simulated_proj:,.2f}."
        )
        if violates_buffer:
            impact_summary += f" This violates your safety buffer of INR {state.minimum_cash_buffer:,.2f} by INR {deficit:,.2f}."

        return SimulationResult(
            user_id=sim_req.user_id,
            scenario_type=sim_req.scenario_type,
            baseline_projected_balance=baseline_proj,
            simulated_projected_balance=simulated_proj,
            buffer_violation_risk=violates_buffer,
            impact_summary=impact_summary,
            goal_impacts=[
                {
                    "goal_id": "goal_vacation_02",
                    "title": "Annual Family Vacation",
                    "delay_months": 1,
                    "impact": "Requires pausing contribution for 30 days to protect cash reserves"
                }
            ],
            recommendation="Maintain emergency buffer by deferring discretionary allocations and non-essential savings goals."
        )

    def get_dashboard(self, user_id: str) -> DashboardResponse:
        state = self.get_current_financial_state(user_id)
        forecast = BalanceForecaster.forecast_30_days(state, scheduled_bills=repo.get_bills(user_id))
        recent_txns = repo.get_transactions(user_id)[:10]

        agent_req = AgentRequest(user_id=user_id)
        latest_advice = self.agent.run(agent_req, state)

        return DashboardResponse(
            user_id=user_id,
            financial_state=state,
            latest_recommendation=latest_advice,
            recent_transactions=recent_txns,
            active_risks=state.risk_signals,
            active_opportunities=state.opportunity_signals,
            forecast_30_days=forecast
        )


# Global orchestrator singleton
orchestrator = FinancialOrchestrator()
