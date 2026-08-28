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
        target_emergency = (
            state.user_preferences.target_emergency_fund_months
            if state.user_preferences
            else 3.0
        )
        target_savings_rate = 0.20

        evidence_list = [
            Evidence(
                metric="current_balance",
                value=round(state.current_balance, 2),
                threshold=None,
                status=UncertaintyStatus.CONFIRMED,
                description="Liquid bank balance after recent transactions",
            ),
            Evidence(
                metric="available_cash",
                value=round(state.available_cash, 2),
                threshold=state.upcoming_obligations,
                status=UncertaintyStatus.CONFIRMED,
                description="Immediate cash available after deducting immediate obligations",
            ),
            Evidence(
                metric="projected_balance",
                value=round(state.projected_balance, 2),
                threshold=round(state.minimum_cash_buffer, 2),
                status=UncertaintyStatus.ESTIMATED,
                description="Deterministic 30-day projected end-of-month cash balance",
            ),
            Evidence(
                metric="minimum_cash_buffer",
                value=round(state.minimum_cash_buffer, 2),
                threshold=None,
                status=UncertaintyStatus.CONFIRMED,
                description="User preference target minimum safety buffer",
            ),
            Evidence(
                metric="upcoming_obligations",
                value=round(state.upcoming_obligations, 2),
                threshold=None,
                status=UncertaintyStatus.CONFIRMED,
                description="Scheduled committed bills due in next 30 days",
            ),
            Evidence(
                metric="emergency_fund_months",
                value=round(state.emergency_fund_months, 2),
                threshold=target_emergency,
                status=UncertaintyStatus.ESTIMATED,
                description="Emergency reserve coverage in months of fixed costs",
            ),
            Evidence(
                metric="savings_rate",
                value=round(state.savings_rate, 4),
                threshold=target_savings_rate,
                status=UncertaintyStatus.ESTIMATED,
                description="Current monthly net savings rate",
            ),
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
            "opportunities": [o.model_dump() for o in opportunities],
        }

