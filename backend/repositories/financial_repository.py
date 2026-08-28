import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

from shared.contracts.contracts import (
    Transaction,
    IncomeRecord,
    Bill,
    FinancialGoal,
    UserPreferences,
    FinancialEvent,
    TransactionType,
    TransactionCategory,
    AgentResponse,
    Recommendation,
    Evidence,
    UncertaintyStatus,
)
from backend.models.database import (
    SessionLocal,
    init_db,
    UserModel,
    AccountModel,
    TransactionModel,
    IncomeRecordModel,
    BillModel,
    FinancialGoalModel,
    UserPreferencesModel,
    FinancialEventModel,
    AgentMemoryModel,
)

logger = logging.getLogger(__name__)


class FinancialRepository:
    """
    Hybrid SQL & In-Memory Financial Repository with Long-Term Agent Memory.
    Persists data to PostgreSQL/Supabase (or SQLite) while providing high-performance access.
    """

    def __init__(self):
        self.transactions: Dict[str, List[Transaction]] = {}
        self.income_records: Dict[str, List[IncomeRecord]] = {}
        self.bills: Dict[str, List[Bill]] = {}
        self.goals: Dict[str, List[FinancialGoal]] = {}
        self.preferences: Dict[str, UserPreferences] = {}
        self.events: Dict[str, List[FinancialEvent]] = {}
        self.memories: Dict[str, List[AgentResponse]] = {}
        self.balances: Dict[str, float] = {}

        # Initialize SQL schema
        try:
            init_db()
        except Exception as e:
            logger.warning(f"Database initialization notice: {e}")

        self.reset()

    def reset(self, user_id: Optional[str] = None):
        """
        Resets repository state and seeds the canonical demo dataset.
        """
        if user_id:
            self._seed_demo_user(user_id)
        else:
            self.transactions.clear()
            self.income_records.clear()
            self.bills.clear()
            self.goals.clear()
            self.preferences.clear()
            self.events.clear()
            self.memories.clear()
            self.balances.clear()
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
                due_date=datetime.now(timezone.utc) + timedelta(days=6),
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
                target_date=datetime.now(timezone.utc) + timedelta(days=120),
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
                target_date=datetime.now(timezone.utc) + timedelta(days=90),
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
            monthly_savings_target=15000.0,
            financial_priorities=["liquidity_preservation", "emergency_fund", "debt_reduction", "investments"]
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
                timestamp=datetime.now(timezone.utc) - timedelta(days=25),
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
                timestamp=datetime.now(timezone.utc) - timedelta(days=20),
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
                timestamp=datetime.now(timezone.utc) - timedelta(days=12),
                source="receipt",
                confidence=0.95,
                is_recurring=False
            )
        ]

        self.events[user_id] = []
        self.memories[user_id] = []

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

        # Persist to SQL if available
        try:
            with SessionLocal() as session:
                user = session.query(UserModel).filter_by(user_id=user_id).first()
                if not user:
                    session.add(UserModel(user_id=user_id, email=f"{user_id}@fidel.finance"))
                db_txn = TransactionModel(
                    transaction_id=txn.transaction_id,
                    user_id=user_id,
                    account_id=txn.account_id,
                    amount=txn.amount,
                    currency=txn.currency,
                    type=txn.type.value if hasattr(txn.type, "value") else str(txn.type),
                    category=txn.category.value if hasattr(txn.category, "value") else str(txn.category),
                    description=txn.description,
                    timestamp=txn.timestamp,
                    source=txn.source,
                    confidence=txn.confidence,
                    is_recurring=txn.is_recurring,
                )
                session.merge(db_txn)
                session.commit()
        except Exception as e:
            logger.debug(f"SQL transaction sync notice: {e}")

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

        # Persist to SQL if available
        try:
            with SessionLocal() as session:
                user = session.query(UserModel).filter_by(user_id=user_id).first()
                if not user:
                    session.add(UserModel(user_id=user_id, email=f"{user_id}@fidel.finance"))
                db_event = FinancialEventModel(
                    event_id=event.event_id,
                    user_id=user_id,
                    event_type=event.event_type,
                    timestamp=event.timestamp,
                    source=event.source,
                    confidence=event.confidence,
                    payload=event.payload,
                )
                session.merge(db_event)
                session.commit()
        except Exception as e:
            logger.debug(f"SQL event sync notice: {e}")

    # --- Long-Term Agent Memory Storage & Retrieval ---

    def save_agent_memory(self, user_id: str, response: AgentResponse, user_query: Optional[str] = None):
        """
        Saves an AgentResponse into Long-Term Memory (in-memory and database).
        """
        if user_id not in self.memories:
            self.memories[user_id] = []
        self.memories[user_id].insert(0, response)

        # Persist to SQL AgentMemoryModel
        try:
            with SessionLocal() as session:
                user = session.query(UserModel).filter_by(user_id=user_id).first()
                if not user:
                    session.add(UserModel(user_id=user_id, email=f"{user_id}@fidel.finance"))

                memory_entry = AgentMemoryModel(
                    memory_id=f"mem_{response.response_id}",
                    user_id=user_id,
                    response_id=response.response_id,
                    user_query=user_query,
                    recommendation_id=response.recommendation.recommendation_id,
                    recommendation_title=response.recommendation.title,
                    recommendation_priority=response.recommendation.priority,
                    recommendation_category=response.recommendation.category,
                    recommendation_description=response.recommendation.description,
                    impact_amount=response.recommendation.impact_amount,
                    reason=response.reason,
                    confidence=response.confidence,
                    evidence_snapshot=[e.model_dump() for e in response.evidence],
                    alternatives=response.alternatives,
                    competing_objectives=response.competing_objectives_considered,
                    created_at=response.generated_at,
                )
                session.merge(memory_entry)
                session.commit()
        except Exception as e:
            logger.debug(f"SQL memory sync notice: {e}")

    def get_agent_memories(self, user_id: str, limit: int = 10) -> List[AgentResponse]:
        """
        Retrieves historical agent decision memories for a user.
        """
        if user_id in self.memories and self.memories[user_id]:
            return self.memories[user_id][:limit]

        # Fetch from SQL if available
        try:
            with SessionLocal() as session:
                entries = (
                    session.query(AgentMemoryModel)
                    .filter_by(user_id=user_id)
                    .order_by(AgentMemoryModel.created_at.desc())
                    .limit(limit)
                    .all()
                )
                results: List[AgentResponse] = []
                for m in entries:
                    evidence_objs = [
                        Evidence(
                            metric=ev.get("metric", "unknown"),
                            value=ev.get("value", 0.0),
                            threshold=ev.get("threshold"),
                            status=UncertaintyStatus(ev.get("status", "confirmed")),
                            description=ev.get("description"),
                        )
                        for ev in (m.evidence_snapshot or [])
                    ]
                    rec = Recommendation(
                        recommendation_id=m.recommendation_id,
                        title=m.recommendation_title,
                        priority=m.recommendation_priority,
                        description=m.recommendation_description,
                        impact_amount=m.impact_amount,
                        category=m.recommendation_category,
                    )
                    results.append(
                        AgentResponse(
                            response_id=m.response_id,
                            user_id=m.user_id,
                            recommendation=rec,
                            reason=m.reason,
                            evidence=evidence_objs,
                            confidence=m.confidence,
                            alternatives=m.alternatives or [],
                            competing_objectives_considered=m.competing_objectives or [],
                            generated_at=m.created_at,
                        )
                    )
                return results
        except Exception as e:
            logger.debug(f"SQL memory fetch notice: {e}")
            return []


# Global repository singleton instance
repo = FinancialRepository()
InMemoryFinancialRepository = FinancialRepository
