from datetime import datetime, timezone
from typing import List, Optional
from shared.contracts.contracts import (
    FinancialState,
    Forecast,
    RiskSignal,
    RiskType,
    RiskSeverity,
    OpportunitySignal,
    OpportunityType,
)


class RiskDetector:
    """
    Authoritative deterministic detector for proactive financial risks,
    liquidity breaches, and goal deficit triggers.
    """

    @staticmethod
    def _to_utc(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @classmethod
    def detect_risks(
        cls,
        state: FinancialState,
        forecast: Optional[Forecast] = None,
    ) -> List[RiskSignal]:
        """
        Evaluates state and forecast against deterministic risk heuristics.
        """
        risks: List[RiskSignal] = []
        now = cls._to_utc(state.generated_at)
        ts_int = int(now.timestamp())
        user_id = state.user_id

        # 1. Liquidity Risk: Projected balance violates minimum cash buffer
        min_proj = forecast.minimum_projected_balance if forecast else state.projected_balance
        eval_proj = min(state.projected_balance, min_proj)

        if eval_proj < state.minimum_cash_buffer:
            deficit = round(state.minimum_cash_buffer - eval_proj, 2)
            if eval_proj <= 0 or deficit >= 15000:
                severity = RiskSeverity.CRITICAL
            elif deficit >= 5000:
                severity = RiskSeverity.MEDIUM
            else:
                severity = RiskSeverity.LOW

            sig_id = f"risk_liq_{abs(hash(f'{user_id}_liq_{eval_proj}')) % 1000000:06d}_{ts_int}"
            risks.append(
                RiskSignal(
                    signal_id=sig_id,
                    type=RiskType.LIQUIDITY,
                    severity=severity,
                    title="Projected Cash Deficit Against Buffer",
                    description=(
                        f"Projected month-end balance (INR {eval_proj:,.2f}) violates your "
                        f"minimum preferred reserve threshold (INR {state.minimum_cash_buffer:,.2f}) by "
                        f"INR {deficit:,.2f}."
                    ),
                    amount_impact=deficit,
                    detected_at=now,
                    is_active=True,
                )
            )

        # 2. Upcoming Obligation Gap: Available cash is insufficient for pending bills
        if state.available_cash < state.upcoming_obligations:
            gap = round(state.upcoming_obligations - state.available_cash, 2)
            severity = RiskSeverity.CRITICAL if state.available_cash <= 0 else RiskSeverity.HIGH
            sig_id = f"risk_oblg_{abs(hash(f'{user_id}_oblg_{gap}')) % 1000000:06d}_{ts_int}"
            risks.append(
                RiskSignal(
                    signal_id=sig_id,
                    type=RiskType.UPCOMING_OBLIGATION,
                    severity=severity,
                    title="Upcoming Obligation Cash Gap",
                    description=(
                        f"Immediate available cash (INR {state.available_cash:,.2f}) is insufficient to "
                        f"cover upcoming 30-day obligations (INR {state.upcoming_obligations:,.2f}) by INR {gap:,.2f}."
                    ),
                    amount_impact=gap,
                    detected_at=now,
                    is_active=True,
                )
            )

        # 3. Emergency Fund Depletion
        target_months = (
            state.user_preferences.target_emergency_fund_months
            if state.user_preferences else 3.0
        )
        if state.emergency_fund_months < 1.0:
            deficit_months = round(target_months - state.emergency_fund_months, 1)
            deficit_amount = round(deficit_months * state.fixed_expenses, 2)
            severity = RiskSeverity.CRITICAL if state.emergency_fund_months < 0.5 else RiskSeverity.HIGH
            sig_id = f"risk_emg_{abs(hash(f'{user_id}_emg_{state.emergency_fund_months}')) % 1000000:06d}_{ts_int}"
            risks.append(
                RiskSignal(
                    signal_id=sig_id,
                    type=RiskType.EMERGENCY_FUND_DEPLETION,
                    severity=severity,
                    title="Depleted Emergency Reserve",
                    description=(
                        f"Current liquid reserve provides {state.emergency_fund_months} months of fixed cost "
                        f"coverage, below your target threshold of {target_months} months."
                    ),
                    amount_impact=deficit_amount if deficit_amount > 0 else None,
                    detected_at=now,
                    is_active=True,
                )
            )

        # 4. Spending Spike Trigger
        if state.discretionary_expenses > 12000.0 or (
            state.expected_monthly_income > 0
            and (state.variable_expenses + state.discretionary_expenses) > state.expected_monthly_income * 0.70
        ):
            excess = round(state.discretionary_expenses - 8000.0, 2)
            sig_id = f"risk_spike_{abs(hash(f'{user_id}_spike_{excess}')) % 1000000:06d}_{ts_int}"
            risks.append(
                RiskSignal(
                    signal_id=sig_id,
                    type=RiskType.SPENDING_SPIKE,
                    severity=RiskSeverity.HIGH if state.discretionary_expenses > 15000 else RiskSeverity.MEDIUM,
                    title="Elevated Discretionary Spend Rate",
                    description=(
                        f"Discretionary and lifestyle spend (INR {state.discretionary_expenses:,.2f}) is "
                        f"trending significantly above standard monthly baseline."
                    ),
                    amount_impact=excess if excess > 0 else None,
                    detected_at=now,
                    is_active=True,
                )
            )

        # 5. Income Reduction / Volatility Trigger
        if state.income_variability > 0.20 or state.income_confidence < 0.75:
            volatility_exposure = round(state.expected_monthly_income * state.income_variability, 2)
            sig_id = f"risk_inc_{abs(hash(f'{user_id}_inc_{volatility_exposure}')) % 1000000:06d}_{ts_int}"
            risks.append(
                RiskSignal(
                    signal_id=sig_id,
                    type=RiskType.INCOME_REDUCTION,
                    severity=RiskSeverity.MEDIUM,
                    title="Income Stream Volatility",
                    description=(
                        f"Income predictability is subject to {int(state.income_variability * 100)}% variance "
                        f"or unconfirmed extraction confidence."
                    ),
                    amount_impact=volatility_exposure if volatility_exposure > 0 else None,
                    detected_at=now,
                    is_active=True,
                )
            )

        # 6. Goal Pacing Deficit Trigger
        at_risk_goals = [g for g in state.financial_goals if g.status in ["at_risk", "behind"]]
        if at_risk_goals:
            total_goal_deficit = round(sum(g.monthly_contribution_required for g in at_risk_goals), 2)
            has_p1 = any(g.priority == 1 for g in at_risk_goals)
            sig_id = f"risk_goal_{abs(hash(f'{user_id}_goal_{total_goal_deficit}')) % 1000000:06d}_{ts_int}"
            risks.append(
                RiskSignal(
                    signal_id=sig_id,
                    type=RiskType.GOAL_DEFICIT,
                    severity=RiskSeverity.HIGH if has_p1 else RiskSeverity.MEDIUM,
                    title="Financial Goal Pacing Deficit",
                    description=(
                        f"{len(at_risk_goals)} active financial goal(s) require INR {total_goal_deficit:,.2f}/mo "
                        f"exceeding currently available monthly surplus."
                    ),
                    amount_impact=total_goal_deficit,
                    detected_at=now,
                    is_active=True,
                )
            )

        return risks


class OpportunityDetector:
    """
    Authoritative deterministic detector for expense reductions,
    surplus allocations, and goal acceleration opportunities.
    """

    @staticmethod
    def _to_utc(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @classmethod
    def detect_opportunities(
        cls,
        state: FinancialState,
        forecast: Optional[Forecast] = None,
    ) -> List[OpportunitySignal]:
        """
        Evaluates state for capital efficiency and savings opportunities.
        """
        opportunities: List[OpportunitySignal] = []
        now = cls._to_utc(state.generated_at)
        ts_int = int(now.timestamp())
        user_id = state.user_id

        # 1. Discretionary Spend Reduction Cushion
        if state.discretionary_expenses > 4000.0:
            potential_saving = round(state.discretionary_expenses * 0.40, 2)
            sig_id = f"opp_disc_{abs(hash(f'{user_id}_disc_{potential_saving}')) % 1000000:06d}_{ts_int}"
            opportunities.append(
                OpportunitySignal(
                    opportunity_id=sig_id,
                    type=OpportunityType.EXPENSE_REDUCTION,
                    title="Discretionary Spend Cushion",
                    description=(
                        f"Trimming discretionary spend by INR {potential_saving:,.2f} this cycle will "
                        f"reinforce liquid reserves and mitigate liquidity deficits."
                    ),
                    potential_benefit_amount=potential_saving,
                    detected_at=now,
                )
            )

        # 2. Surplus Capital Allocation
        if state.projected_balance > state.minimum_cash_buffer + 10000.0:
            surplus = round(state.projected_balance - state.minimum_cash_buffer, 2)
            sig_id = f"opp_surplus_{abs(hash(f'{user_id}_surplus_{surplus}')) % 1000000:06d}_{ts_int}"
            opportunities.append(
                OpportunitySignal(
                    opportunity_id=sig_id,
                    type=OpportunityType.SURPLUS_ALLOCATION,
                    title="Surplus Capital Deployment",
                    description=(
                        f"Projected month-end surplus of INR {surplus:,.2f} above minimum buffer "
                        f"can be deployed to accelerate investments or high-priority goals."
                    ),
                    potential_benefit_amount=surplus,
                    detected_at=now,
                )
            )

        # 3. Goal Acceleration
        on_track_goals = [g for g in state.financial_goals if g.status == "on_track"]
        if state.savings_rate >= 0.20 and on_track_goals:
            acceleration_amount = round(state.expected_monthly_income * 0.10, 2)
            sig_id = f"opp_goal_{abs(hash(f'{user_id}_acc_{acceleration_amount}')) % 1000000:06d}_{ts_int}"
            opportunities.append(
                OpportunitySignal(
                    opportunity_id=sig_id,
                    type=OpportunityType.GOAL_ACCELERATION,
                    title="Strategic Goal Acceleration",
                    description=(
                        f"Healthy savings rate of {int(state.savings_rate * 100)}% enables allocating an additional "
                        f"INR {acceleration_amount:,.2f}/mo toward {on_track_goals[0].title}."
                    ),
                    potential_benefit_amount=acceleration_amount,
                    detected_at=now,
                )
            )

        # 4. High-Yield Savings Deployment
        if state.current_balance > state.minimum_cash_buffer + 25000.0:
            idle_capital = state.current_balance - state.minimum_cash_buffer
            interest_benefit = round(idle_capital * 0.07, 2)
            sig_id = f"opp_hys_{abs(hash(f'{user_id}_hys_{interest_benefit}')) % 1000000:06d}_{ts_int}"
            opportunities.append(
                OpportunitySignal(
                    opportunity_id=sig_id,
                    type=OpportunityType.HIGH_YIELD_SAVINGS,
                    title="Idle Cash Yield Optimization",
                    description=(
                        f"Moving INR {idle_capital:,.2f} in excess liquid cash to an auto-sweep or high-yield "
                        f"savings account could generate ~INR {interest_benefit:,.2f} annually."
                    ),
                    potential_benefit_amount=interest_benefit,
                    detected_at=now,
                )
            )

        return opportunities

