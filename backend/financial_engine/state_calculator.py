from datetime import datetime, timedelta, timezone
from typing import List, Optional
from shared.contracts.contracts import (
    FinancialGoal,
    FinancialState,
    IncomeRecord,
    Bill,
    Transaction,
    TransactionCategory,
    TransactionType,
    UserPreferences,
)
from backend.financial_engine.risk_detector import RiskDetector, OpportunityDetector


class FinancialStateCalculator:
    """
    Authoritative deterministic calculator for FinancialState.
    Computes canonical mathematical state from heterogeneous financial records,
    income profiles, bills, active goals, and user preferences.
    """

    FREQUENCY_MULTIPLIERS = {
        "monthly": 1.0,
        "biweekly": 26.0 / 12.0,
        "weekly": 52.0 / 12.0,
        "quarterly": 4.0 / 12.0,
        "semi-annual": 2.0 / 12.0,
        "annual": 1.0 / 12.0,
        "yearly": 1.0 / 12.0,
        "irregular": 1.0,
    }

    @staticmethod
    def _to_utc(dt: datetime) -> datetime:
        """Ensures a datetime object is timezone-aware in UTC."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @classmethod
    def calculate_state(
        cls,
        user_id: str,
        current_balance: float,
        transactions: List[Transaction],
        income_records: List[IncomeRecord],
        bills: List[Bill],
        goals: List[FinancialGoal],
        preferences: Optional[UserPreferences] = None,
        investments_total_value: float = 0.0,
        liquid_savings: float = 0.0,
        as_of: Optional[datetime] = None,
        populate_signals: bool = True,
    ) -> FinancialState:
        """
        Deterministically calculates the single source of truth FinancialState.
        """
        ref_time = cls._to_utc(as_of) if as_of else datetime.now(timezone.utc)

        if preferences is None:
            preferences = UserPreferences(user_id=user_id)

        # 1. Deterministic Monthly Income Calculation
        expected_monthly_income = 0.0
        income_variability = 0.05
        income_confidence = 0.95

        if income_records:
            total_normalized_income = 0.0
            weighted_variability = 0.0
            weighted_confidence = 0.0
            total_nominal_income = 0.0

            for inc in income_records:
                mult = cls.FREQUENCY_MULTIPLIERS.get(inc.frequency.lower(), 1.0)
                monthly_amt = inc.amount * mult
                total_normalized_income += monthly_amt
                total_nominal_income += inc.amount
                weighted_variability += inc.variability * inc.amount
                weighted_confidence += inc.confidence * inc.amount

            expected_monthly_income = round(total_normalized_income, 2)
            if total_nominal_income > 0:
                income_variability = round(weighted_variability / total_nominal_income, 2)
                income_confidence = round(weighted_confidence / total_nominal_income, 2)
        else:
            # Fallback: estimate from recent income transactions
            income_txns = [
                t for t in transactions
                if t.type == TransactionType.CREDIT or t.category == TransactionCategory.INCOME
            ]
            if income_txns:
                expected_monthly_income = round(sum(t.amount for t in income_txns), 2)
                income_confidence = round(sum(t.confidence for t in income_txns) / len(income_txns), 2)

        # 2. Categorize Expenses from Recent Transactions
        fixed_expenses = 0.0
        variable_expenses = 0.0
        discretionary_expenses = 0.0

        for txn in transactions:
            if txn.type == TransactionType.DEBIT:
                if txn.category in [
                    TransactionCategory.HOUSING,
                    TransactionCategory.UTILITIES,
                    TransactionCategory.DEBT_SERVICE,
                ]:
                    fixed_expenses += txn.amount
                elif txn.category in [
                    TransactionCategory.GROCERIES,
                    TransactionCategory.HEALTHCARE,
                    TransactionCategory.TRANSPORTATION,
                ]:
                    variable_expenses += txn.amount
                elif txn.category in [
                    TransactionCategory.DINING,
                    TransactionCategory.ENTERTAINMENT,
                    TransactionCategory.SHOPPING,
                    TransactionCategory.OTHER,
                ]:
                    discretionary_expenses += txn.amount
                elif txn.category == TransactionCategory.UNEXPECTED:
                    # Unexpected expense is tracked in ledger but excluded from ongoing recurring baseline
                    pass

        # Fallback to realistic defaults if transaction ledger is empty
        if not transactions:
            if bills:
                fixed_expenses = sum(
                    b.amount for b in bills
                    if b.category in [TransactionCategory.HOUSING, TransactionCategory.UTILITIES, TransactionCategory.DEBT_SERVICE]
                )
            if fixed_expenses == 0.0:
                fixed_expenses = 24000.0
            if variable_expenses == 0.0:
                variable_expenses = 12000.0
            if discretionary_expenses == 0.0:
                discretionary_expenses = 8500.0

        fixed_expenses = round(fixed_expenses, 2)
        variable_expenses = round(variable_expenses, 2)
        discretionary_expenses = round(discretionary_expenses, 2)

        # 3. Upcoming Obligations (Next 30 Days)
        thirty_days = ref_time + timedelta(days=30)
        unpaid_30d_bills = [
            b for b in bills
            if not b.is_paid and cls._to_utc(b.due_date) <= thirty_days
        ]
        upcoming_obligations = round(sum(b.amount for b in unpaid_30d_bills), 2)
        if upcoming_obligations == 0.0 and not bills:
            upcoming_obligations = 18000.0

        # 4. Immediate Unpaid Bills (Next 7 Days) and Liquid Available Cash
        seven_days = ref_time + timedelta(days=7)
        immediate_bills = sum(
            b.amount for b in bills
            if not b.is_paid and cls._to_utc(b.due_date) <= seven_days
        )
        available_cash = round(max(0.0, current_balance - immediate_bills), 2)

        # 5. Emergency Fund Coverage (Months of Fixed Costs)
        monthly_fixed_costs = max(1.0, fixed_expenses if fixed_expenses > 0 else 24000.0)
        emergency_fund_months = round(liquid_savings / monthly_fixed_costs, 1)

        # 6. Savings Rate
        total_monthly_outflow = fixed_expenses + variable_expenses + discretionary_expenses
        savings_rate = 0.0
        if expected_monthly_income > 0:
            savings_rate = round(
                max(0.0, min(1.0, (expected_monthly_income - total_monthly_outflow) / expected_monthly_income)),
                2,
            )

        # 7. Projected Balance (30-Day Cycle-End)
        remaining_cycle_burn = round((variable_expenses + discretionary_expenses) * 0.1, 2)
        projected_balance = round(current_balance - upcoming_obligations - remaining_cycle_burn, 2)

        # 8. Dynamic Financial Goal Pacing
        monthly_surplus = max(0.0, expected_monthly_income - total_monthly_outflow)
        updated_goals: List[FinancialGoal] = []

        for goal in goals:
            target_dt = cls._to_utc(goal.target_date)
            remaining_amount = max(0.0, goal.target_amount - goal.current_amount)
            days_left = max(1, (target_dt - ref_time).days)
            months_left = max(1, round(days_left / 30.4))
            
            # Deterministic required contribution
            if remaining_amount == 0.0:
                required_contrib = 0.0
                status = "achieved"
            else:
                required_contrib = round(remaining_amount / months_left, 2)
                if required_contrib > monthly_surplus and monthly_surplus > 0:
                    status = "at_risk"
                elif goal.status == "at_risk" and required_contrib <= monthly_surplus:
                    status = "on_track"
                else:
                    status = goal.status

            updated_goals.append(
                FinancialGoal(
                    goal_id=goal.goal_id,
                    user_id=goal.user_id,
                    title=goal.title,
                    target_amount=goal.target_amount,
                    current_amount=goal.current_amount,
                    currency=goal.currency,
                    target_date=goal.target_date,
                    monthly_contribution_required=required_contrib if required_contrib > 0 else goal.monthly_contribution_required,
                    priority=goal.priority,
                    status=status,
                )
            )

        # 9. Data Completeness Ratio
        core_dimensions = [
            current_balance > 0,
            expected_monthly_income > 0,
            fixed_expenses > 0,
            len(goals) > 0,
            len(transactions) > 0,
            len(bills) > 0,
            liquid_savings > 0 or investments_total_value > 0,
            preferences is not None,
        ]
        data_completeness = round(sum(1 for d in core_dimensions if d) / len(core_dimensions), 2)

        # 10. Overall System Confidence Score
        avg_txn_confidence = (
            sum(t.confidence for t in transactions) / len(transactions)
            if transactions else 0.95
        )
        overall_confidence = round(
            0.40 * data_completeness + 0.30 * income_confidence + 0.30 * avg_txn_confidence,
            2,
        )

        state = FinancialState(
            user_id=user_id,
            generated_at=ref_time,
            current_balance=current_balance,
            available_cash=available_cash,
            expected_monthly_income=expected_monthly_income,
            income_variability=income_variability,
            income_confidence=income_confidence,
            fixed_expenses=fixed_expenses,
            variable_expenses=variable_expenses,
            discretionary_expenses=discretionary_expenses,
            recurring_obligations=fixed_expenses,
            upcoming_obligations=upcoming_obligations,
            savings=liquid_savings,
            emergency_fund_months=emergency_fund_months,
            savings_rate=savings_rate,
            financial_goals=updated_goals,
            investments_total_value=investments_total_value,
            projected_balance=projected_balance,
            minimum_cash_buffer=preferences.minimum_cash_buffer,
            risk_signals=[],
            opportunity_signals=[],
            user_preferences=preferences,
            data_completeness=data_completeness,
            overall_confidence=overall_confidence,
        )

        # 11. Deterministic Signal Hydration
        if populate_signals:
            state.risk_signals = RiskDetector.detect_risks(state)
            state.opportunity_signals = OpportunityDetector.detect_opportunities(state)

        return state

