from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AccountModel(Base):
    __tablename__ = "accounts"

    account_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    account_name = Column(String, nullable=False)
    account_type = Column(String, default="checking") # checking, savings, credit
    balance = Column(Float, default=0.0)
    currency = Column(String, default="INR")
    updated_at = Column(DateTime, default=datetime.utcnow)


class TransactionModel(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    account_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    type = Column(String, nullable=False) # debit, credit, transfer
    category = Column(String, default="other")
    description = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String, default="manual")
    confidence = Column(Float, default=1.0)
    is_recurring = Column(Boolean, default=False)


class FinancialEventModel(Base):
    __tablename__ = "financial_events"

    event_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    event_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String, default="manual")
    confidence = Column(Float, default=1.0)
    payload = Column(JSON, default=dict)


class FinancialGoalModel(Base):
    __tablename__ = "financial_goals"

    goal_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    currency = Column(String, default="INR")
    target_date = Column(DateTime, nullable=False)
    monthly_contribution_required = Column(Float, default=0.0)
    priority = Column(Integer, default=1)
    status = Column(String, default="on_track")


class BillModel(Base):
    __tablename__ = "bills"

    bill_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    biller_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    due_date = Column(DateTime, nullable=False)
    category = Column(String, default="utilities")
    is_paid = Column(Boolean, default=False)
    is_auto_pay = Column(Boolean, default=False)
