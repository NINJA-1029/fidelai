from typing import Any, Dict, List
from shared.contracts.contracts import (
    FinancialState,
    Evidence,
    UncertaintyStatus,
)
from backend.financial_engine.forecasting import BalanceForecaster
from backend.financial_engine.risk_detector import RiskDetector, OpportunityDetector


class AgentTools:
    """
    Deterministic tools callable by the Agent to gather mathematical facts and evidence.
    """

    @staticmethod
    def gather_evidence_for_liquidity(state: FinancialState) -> List[Evidence]:
        evidence_list = [
            Evidence(
                metric="current_balance",
                value=state.current_balance,
                threshold=None,
                status=UncertaintyStatus.CONFIRMED,
                description="Liquid bank balance"
            ),
            Evidence(
                metric="projected_balance",
                value=state.projected_balance,
                threshold=state.minimum_cash_buffer,
                status=UncertaintyStatus.ESTIMATED,
                description="30-day projected end-of-month cash balance"
            ),
            Evidence(
                metric="minimum_cash_buffer",
                value=state.minimum_cash_buffer,
                threshold=None,
                status=UncertaintyStatus.CONFIRMED,
                description="Configured minimum reserve floor"
            ),
            Evidence(
                metric="upcoming_obligations",
                value=state.upcoming_obligations,
                threshold=None,
                status=UncertaintyStatus.CONFIRMED,
                description="Scheduled bills due in next 30 days"
            )
        ]
        return evidence_list

    @staticmethod
    def run_balance_forecast(state: FinancialState) -> Dict[str, Any]:
        forecast = BalanceForecaster.forecast_30_days(state)
        return forecast.model_dump()

    @staticmethod
    def detect_signals(state: FinancialState) -> Dict[str, Any]:
        risks = RiskDetector.detect_risks(state)
        opportunities = OpportunityDetector.detect_opportunities(state)
        return {
            "risks": [r.model_dump() for r in risks],
            "opportunities": [o.model_dump() for o in opportunities]
        }
