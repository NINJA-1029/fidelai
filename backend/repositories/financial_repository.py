from datetime import datetime, timedelta
from typing import Dict, List, Optional
from shared.contracts.contracts import (
    Transaction,
    IncomeRecord,
    Bill,
    FinancialGoal,
    UserPreferences,
    FinancialEvent,
    TransactionType,
    TransactionCategory,
)


class InMemoryFinancialRepository:
    """
    In-memory financial repository seeded with the canonical demo dataset.
    Provides fast, deterministic access for local testing, CI, and server execution.
    """

    def __init__(self):
        self.transactions: Dict[str, List[Transaction]] = {}
        self.income_records: Dict[str, List[IncomeRecord]] = {}
        self.bills: Dict[str, List[Bill]] = {}
        self.goals: Dict[str, List[FinancialGoal]] = {}
        self.preferences: Dict[str, UserPreferences] = {}
        self.events: Dict[str, List[FinancialEvent]] = {}
        self.balances: Dict[str, float] = {}
        self._seed_demo_user("user_demo_01")

    def _seed_demo_user(self, user_id: str):
        self.balances[user_id] = 42000.0  # Starting balance before unexpected expense

        self.income_records[user_id] = [
            IncomeRecord(
                income_id="inc_001",
                user_id=user_id,
                source_name="Tech Corp Salary",
                amount=65000.0,
                currency="INR",
                frequency="monthly",
                expected_day_of_month=1,
                confidence=1.0,
                variability=0.05
            )
        ]

        self.bills[user_id] = [
            Bill(
                bill_id="bill_001",
                user_id=user_id,
                biller_name="Apartment Rent & Maintenance",
                amount=18000.0,
                currency="INR",
                due_date=datetime.utcnow() + timedelta(days=6),
                category=TransactionCategory.HOUSING,
                is_paid=False,
                is_auto_pay=True
            )
        ]

        self.goals[user_id] = [
            FinancialGoal(
                goal_id="goal_emergency_01",
                user_id=user_id,
                title="Emergency Fund Reserve",
                target_amount=72000.0,
                current_amount=50000.0,
                currency="INR",
                target_date=datetime.utcnow() + timedelta(days=120),
                monthly_contribution_required=5500.0,
                priority=1,
                status="on_track"
            ),
            FinancialGoal(
                goal_id="goal_vacation_02",
                user_id=user_id,
                title="Annual Family Vacation",
                target_amount=40000.0,
                current_amount=15000.0,
                currency="INR",
                target_date=datetime.utcnow() + timedelta(days=90),
                monthly_contribution_required=8333.0,
                priority=3,
                status="at_risk"
            )
        ]

        self.preferences[user_id] = UserPreferences(
            user_id=user_id,
            risk_tolerance="moderate",
            minimum_cash_buffer=25000.0,
            target_emergency_fund_months=3.0,
            monthly_savings_target=15000.0
        )

        self.transactions[user_id] = [
            Transaction(
                transaction_id="tx_001",
                user_id=user_id,
                account_id="acc_checking_01",
                amount=22000.0,
                currency="INR",
                type=TransactionType.DEBIT,
                category=TransactionCategory.HOUSING,
                description="Previous Rent Debit",
                timestamp=datetime.utcnow() - timedelta(days=25),
                source="bank_api",
                confidence=1.0,
                is_recurring=True
            ),
            Transaction(
                transaction_id="tx_002",
                user_id=user_id,
                account_id="acc_checking_01",
                amount=2000.0,
                currency="INR",
                type=TransactionType.DEBIT,
                category=TransactionCategory.UTILITIES,
                description="Electricity & Broadband",
                timestamp=datetime.utcnow() - timedelta(days=20),
                source="bank_api",
                confidence=1.0,
                is_recurring=True
            ),
            Transaction(
                transaction_id="tx_003",
                user_id=user_id,
                account_id="acc_checking_01",
                amount=9000.0,
                currency="INR",
                type=TransactionType.DEBIT,
                category=TransactionCategory.GROCERIES,
                description="Supermarket Provisions",
                timestamp=datetime.utcnow() - timedelta(days=12),
                source="receipt",
                confidence=0.95,
                is_recurring=False
            )
        ]

        self.events[user_id] = []

    def get_balance(self, user_id: str) -> float:
        return self.balances.get(user_id, 30000.0)

    def set_balance(self, user_id: str, new_balance: float):
        self.balances[user_id] = new_balance

    def get_transactions(self, user_id: str) -> List[Transaction]:
        return self.transactions.get(user_id, [])

    def add_transaction(self, user_id: str, txn: Transaction):
        if user_id not in self.transactions:
            self.transactions[user_id] = []
        self.transactions[user_id].insert(0, txn)
        if txn.type == TransactionType.DEBIT:
            self.balances[user_id] = self.get_balance(user_id) - txn.amount
        elif txn.type == TransactionType.CREDIT:
            self.balances[user_id] = self.get_balance(user_id) + txn.amount

    def get_income_records(self, user_id: str) -> List[IncomeRecord]:
        return self.income_records.get(user_id, [])

    def get_bills(self, user_id: str) -> List[Bill]:
        return self.bills.get(user_id, [])

    def get_goals(self, user_id: str) -> List[FinancialGoal]:
        return self.goals.get(user_id, [])

    def get_preferences(self, user_id: str) -> UserPreferences:
        return self.preferences.get(user_id, UserPreferences(user_id=user_id))

    def add_event(self, user_id: str, event: FinancialEvent):
        if user_id not in self.events:
            self.events[user_id] = []
        self.events[user_id].insert(0, event)


# Global repository singleton instance
repo = InMemoryFinancialRepository()
