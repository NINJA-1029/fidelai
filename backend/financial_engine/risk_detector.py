from datetime import datetime
from typing import List
from shared.contracts.contracts import (
    FinancialState,
    RiskSignal,
    RiskType,
    RiskSeverity,
    OpportunitySignal,
    OpportunityType,
)


class RiskDetector:
    """
    Detects deterministic financial risks based on state and projections.
    """

    @staticmethod
    def detect_risks(state: FinancialState) -> List[RiskSignal]:
        risks: List[RiskSignal] = []

        # 1. Liquidity risk: Projected balance falls below minimum cash buffer
        if state.projected_balance < state.minimum_cash_buffer:
            deficit = state.minimum_cash_buffer - state.projected_balance
            severity = RiskSeverity.CRITICAL if state.projected_balance <= 0 else RiskSeverity.MEDIUM
            risks.append(
                RiskSignal(
                    signal_id=f"risk_liq_{int(datetime.utcnow().timestamp())}",
                    type=RiskType.LIQUIDITY,
                    severity=severity,
                    title="Projected Cash Deficit Against Buffer",
                    description=(
                        f"Projected month-end balance (INR {state.projected_balance:,.2f}) violates your "
                        f"minimum preferred reserve threshold (INR {state.minimum_cash_buffer:,.2f}) by "
                        f"INR {deficit:,.2f}."
                    ),
                    amount_impact=deficit,
                    detected_at=datetime.utcnow(),
                    is_active=True
                )
            )

        # 2. Upcoming obligation pressure
        if state.available_cash < state.upcoming_obligations:
            gap = state.upcoming_obligations - state.available_cash
            risks.append(
                RiskSignal(
                    signal_id=f"risk_oblg_{int(datetime.utcnow().timestamp())}",
                    type=RiskType.UPCOMING_OBLIGATION,
                    severity=RiskSeverity.HIGH,
                    title="Upcoming Obligation Cash Gap",
                    description=f"Immediate available cash is insufficient to cover pending bills by INR {gap:,.2f}.",
                    amount_impact=gap,
                    detected_at=datetime.utcnow(),
                    is_active=True
                )
            )

        # 3. Emergency fund depletion
        if state.emergency_fund_months < 1.0:
            risks.append(
                RiskSignal(
                    signal_id=f"risk_emg_{int(datetime.utcnow().timestamp())}",
                    type=RiskType.EMERGENCY_FUND_DEPLETION,
                    severity=RiskSeverity.HIGH,
                    title="Depleted Emergency Reserve",
                    description=f"Current emergency fund covers only {state.emergency_fund_months} months of fixed expenses.",
                    amount_impact=None,
                    detected_at=datetime.utcnow(),
                    is_active=True
                )
            )

        return risks


class OpportunityDetector:
    """
    Detects deterministic financial opportunities and surplus optimization paths.
    """

    @staticmethod
    def detect_opportunities(state: FinancialState) -> List[OpportunitySignal]:
        opportunities: List[OpportunitySignal] = []

        # 1. Discretionary spend reduction opportunity
        if state.discretionary_expenses > 4000:
            potential_saving = round(state.discretionary_expenses * 0.45, 2)
            opportunities.append(
                OpportunitySignal(
                    opportunity_id=f"opp_disc_{int(datetime.utcnow().timestamp())}",
                    type=OpportunityType.EXPENSE_REDUCTION,
                    title="Discretionary Spend Cushion",
                    description=(
                        f"Reducing remaining discretionary spend by INR {potential_saving:,.2f} this month "
                        f"will bolster your projected cash reserves."
                    ),
                    potential_benefit_amount=potential_saving,
                    detected_at=datetime.utcnow()
                )
            )

        # 2. Surplus allocation if projected balance is well above buffer
        if state.projected_balance > state.minimum_cash_buffer + 15000:
            surplus = state.projected_balance - state.minimum_cash_buffer
            opportunities.append(
                OpportunitySignal(
                    opportunity_id=f"opp_surplus_{int(datetime.utcnow().timestamp())}",
                    type=OpportunityType.SURPLUS_ALLOCATION,
                    title="Surplus Capital Deployment",
                    description=f"Projected surplus of INR {surplus:,.2f} can accelerate goal contributions.",
                    potential_benefit_amount=surplus,
                    detected_at=datetime.utcnow()
                )
            )

        return opportunities
