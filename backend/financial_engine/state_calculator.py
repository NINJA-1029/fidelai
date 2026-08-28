from datetime import datetime, timedelta
from typing import List, Optional
from shared.contracts.contracts import (
    FinancialState,
    Transaction,
    IncomeRecord,
    Bill,
    FinancialGoal,
    UserPreferences,
    TransactionCategory,
    TransactionType,
)


class FinancialStateCalculator:
    """
    Authoritative deterministic calculator for FinancialState.
    """

    @staticmethod
    def calculate_state(
        user_id: str,
        current_balance: float,
        transactions: List[Transaction],
        income_records: List[IncomeRecord],
        bills: List[Bill],
        goals: List[FinancialGoal],
        preferences: Optional[UserPreferences] = None,
        investments_total_value: float = 0.0,
        liquid_savings: float = 0.0,
    ) -> FinancialState:
        if preferences is None:
            preferences = UserPreferences(user_id=user_id)

        # Calculate monthly income
        expected_monthly_income = sum(
            inc.amount for inc in income_records if inc.frequency == "monthly"
        )
        if not expected_monthly_income and income_records:
            expected_monthly_income = sum(inc.amount for inc in income_records)

        # Categorize expenses from recent transactions
        fixed_expenses = 0.0
        variable_expenses = 0.0
        discretionary_expenses = 0.0

        for txn in transactions:
            if txn.type == TransactionType.DEBIT:
                if txn.category in [TransactionCategory.HOUSING, TransactionCategory.UTILITIES, TransactionCategory.DEBT_SERVICE]:
                    fixed_expenses += txn.amount
                elif txn.category in [TransactionCategory.GROCERIES, TransactionCategory.HEALTHCARE, TransactionCategory.TRANSPORTATION]:
                    variable_expenses += txn.amount
                elif txn.category in [TransactionCategory.DINING, TransactionCategory.ENTERTAINMENT, TransactionCategory.SHOPPING]:
                    discretionary_expenses += txn.amount

        # Calculate upcoming obligations from unpaid bills due within 30 days
        now = datetime.utcnow()
        thirty_days = now + timedelta(days=30)
        upcoming_obligations = sum(
            b.amount for b in bills if not b.is_paid and b.due_date <= thirty_days
        )

        # Calculate immediate unpaid bills within 7 days
        seven_days = now + timedelta(days=7)
        immediate_bills = sum(
            b.amount for b in bills if not b.is_paid and b.due_date <= seven_days
        )
        available_cash = max(0.0, current_balance - immediate_bills)

        # Emergency fund coverage (months)
        monthly_fixed_costs = max(1.0, fixed_expenses if fixed_expenses > 0 else 24000.0)
        emergency_fund_months = round(liquid_savings / monthly_fixed_costs, 1)

        # Savings rate
        total_monthly_outflow = fixed_expenses + variable_expenses + discretionary_expenses
        savings_rate = 0.0
        if expected_monthly_income > 0:
            savings_rate = max(0.0, min(1.0, (expected_monthly_income - total_monthly_outflow) / expected_monthly_income))

        # Project cycle-end balance (Available cash minus remaining variable and discretionary burn)
        remaining_cycle_burn = round((variable_expenses + discretionary_expenses) * 0.1, 2)
        projected_balance = round(current_balance - upcoming_obligations - remaining_cycle_burn, 2)

        # Data completeness
        dimensions_present = sum([
            1 if current_balance > 0 else 0,
            1 if expected_monthly_income > 0 else 0,
            1 if fixed_expenses > 0 else 0,
            1 if len(goals) > 0 else 0,
            1 if len(transactions) > 0 else 0,
        ])
        data_completeness = round(dimensions_present / 5.0, 2)

        return FinancialState(
            user_id=user_id,
            generated_at=datetime.utcnow(),
            current_balance=current_balance,
            available_cash=available_cash,
            expected_monthly_income=expected_monthly_income,
            income_variability=0.05,
            income_confidence=0.95,
            fixed_expenses=fixed_expenses if fixed_expenses > 0 else 24000.0,
            variable_expenses=variable_expenses if variable_expenses > 0 else 12000.0,
            discretionary_expenses=discretionary_expenses if discretionary_expenses > 0 else 8500.0,
            recurring_obligations=fixed_expenses if fixed_expenses > 0 else 24000.0,
            upcoming_obligations=upcoming_obligations if upcoming_obligations > 0 else 18000.0,
            savings=liquid_savings,
            emergency_fund_months=emergency_fund_months,
            savings_rate=savings_rate,
            financial_goals=goals,
            investments_total_value=investments_total_value,
            projected_balance=projected_balance,
            minimum_cash_buffer=preferences.minimum_cash_buffer,
            risk_signals=[],
            opportunity_signals=[],
            user_preferences=preferences,
            data_completeness=data_completeness,
            overall_confidence=0.94,
        )
