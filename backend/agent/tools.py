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

    @staticmethod
    def gather_tradeoff_context(state: FinancialState) -> Dict[str, Any]:
        """
        Extracts structured mathematical trade-off dimensions across:
        1. Liquidity preservation vs. safety buffer floor
        2. Goal contributions by priority ranking
        3. Investment portfolio compounding vs. liquidation
        4. Discretionary spending reduction capacity
        """
        shortfall = max(0.0, round(state.minimum_cash_buffer - state.projected_balance, 2))
        surplus = max(0.0, round(state.projected_balance - state.minimum_cash_buffer, 2))

        goals_sorted = sorted(state.financial_goals, key=lambda g: g.priority)
        total_monthly_goal_req = sum(g.monthly_contribution_required for g in state.financial_goals)

        return {
            "is_deficit": shortfall > 0.0,
            "shortfall_amount": shortfall,
            "surplus_amount": surplus,
            "total_monthly_goal_allocation": round(total_monthly_goal_req, 2),
            "goals_ranked": [
                {
                    "goal_id": g.goal_id,
                    "title": g.title,
                    "priority": g.priority,
                    "monthly_req": round(g.monthly_contribution_required, 2),
                    "current_amount": round(g.current_amount, 2),
                    "target_amount": round(g.target_amount, 2),
                }
                for g in goals_sorted
            ],
            "discretionary_expenses": round(state.discretionary_expenses, 2),
            "investments_total_value": round(state.investments_total_value, 2),
            "savings": round(state.savings, 2),
        }
