import os
from datetime import datetime, timezone
from typing import Generator
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Base declarative class
Base = declarative_base()


# --- Database Connection and Engine Configuration ---

def get_database_url() -> str:
    """
    Resolves the active database connection string.
    Prioritizes Supabase / PostgreSQL DATABASE_URL, with seamless fallback to SQLite.
    """
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        # Fix for SQLAlchemy 2.0 requiring postgresql:// instead of postgres://
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    if not db_url:
        db_url = os.getenv("SUPABASE_DB_URL") or "sqlite:///./fidel.db"
    return db_url


DATABASE_URL = get_database_url()
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a managed database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initializes all defined database tables.
    """
    Base.metadata.create_all(bind=engine)


# --- Relational Database Models ---

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(String(64), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AccountModel(Base):
    __tablename__ = "accounts"

    account_id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False, index=True)
    account_name = Column(String(128), nullable=False)
    account_type = Column(String(32), default="checking")  # checking, savings, credit, investment
    balance = Column(Float, default=0.0)
    currency = Column(String(8), default="INR")
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class TransactionModel(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False, index=True)
    account_id = Column(String(64), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(8), default="INR")
    type = Column(String(16), nullable=False)  # debit, credit, transfer
    category = Column(String(32), default="other")
    description = Column(String(512), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    source = Column(String(32), default="manual")  # bank_api, sms, receipt, manual, csv
    confidence = Column(Float, default=1.0)
    is_recurring = Column(Boolean, default=False)


class IncomeRecordModel(Base):
    __tablename__ = "income_records"

    income_id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False, index=True)
    source_name = Column(String(128), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(8), default="INR")
    frequency = Column(String(32), default="monthly")
    expected_day_of_month = Column(Integer, nullable=True)
    confidence = Column(Float, default=1.0)
    variability = Column(Float, default=0.0)


class BillModel(Base):
    __tablename__ = "bills"

    bill_id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False, index=True)
    biller_name = Column(String(128), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(8), default="INR")
    due_date = Column(DateTime, nullable=False, index=True)
    category = Column(String(32), default="utilities")
    is_paid = Column(Boolean, default=False)
    is_auto_pay = Column(Boolean, default=False)


class FinancialGoalModel(Base):
    __tablename__ = "financial_goals"

    goal_id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False, index=True)
    title = Column(String(128), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    currency = Column(String(8), default="INR")
    target_date = Column(DateTime, nullable=False)
    monthly_contribution_required = Column(Float, default=0.0)
    priority = Column(Integer, default=1)
    status = Column(String(32), default="on_track")


class UserPreferencesModel(Base):
    __tablename__ = "user_preferences"

    user_id = Column(String(64), primary_key=True, index=True)
    risk_tolerance = Column(String(32), default="moderate")
    minimum_cash_buffer = Column(Float, default=25000.0)
    target_emergency_fund_months = Column(Float, default=3.0)
    monthly_savings_target = Column(Float, default=15000.0)
    financial_priorities = Column(JSON, default=list)


class FinancialEventModel(Base):
    __tablename__ = "financial_events"

    event_id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    source = Column(String(32), default="manual")
    confidence = Column(Float, default=1.0)
    payload = Column(JSON, default=dict)


class AgentMemoryModel(Base):
    """
    Long-Term Memory table storing historical AI advisor recommendations,
    evidence snapshots, evaluated tradeoffs, and user queries.
    """
    __tablename__ = "agent_memories"

    memory_id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=False, index=True)
    response_id = Column(String(64), nullable=False, index=True)
    user_query = Column(Text, nullable=True)
    recommendation_id = Column(String(64), nullable=False)
    recommendation_title = Column(String(256), nullable=False)
    recommendation_priority = Column(String(32), nullable=False)
    recommendation_category = Column(String(32), nullable=False)
    recommendation_description = Column(Text, nullable=False)
    impact_amount = Column(Float, nullable=True)
    reason = Column(Text, nullable=False)
    confidence = Column(Float, default=0.90)
    evidence_snapshot = Column(JSON, default=list)
    alternatives = Column(JSON, default=list)
    competing_objectives = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
