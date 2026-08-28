"""
Shared Pydantic contracts for the Agentic AI Financial Management System.
All modules (Ingestion, Financial Engine, Agent, FastAPI, and Frontend) adhere strictly
to these canonical data models.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- Enums ---

class UncertaintyStatus(str, Enum):
    CONFIRMED = "confirmed"
    ESTIMATED = "estimated"
    UNCERTAIN = "uncertain"
    UNKNOWN = "unknown"


class TransactionType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"
    TRANSFER = "transfer"


class TransactionCategory(str, Enum):
    INCOME = "income"
    HOUSING = "housing"
    UTILITIES = "utilities"
    GROCERIES = "groceries"
    DINING = "dining"
    TRANSPORTATION = "transportation"
    HEALTHCARE = "healthcare"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    INVESTMENT = "investment"
    SAVINGS = "savings"
    DEBT_SERVICE = "debt_service"
    UNEXPECTED = "unexpected"
    OTHER = "other"


class RiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskType(str, Enum):
    LIQUIDITY = "liquidity"
    SPENDING_SPIKE = "spending_spike"
    INCOME_REDUCTION = "income_reduction"
    GOAL_DEFICIT = "goal_deficit"
    UPCOMING_OBLIGATION = "upcoming_obligation"
    EMERGENCY_FUND_DEPLETION = "emergency_fund_depletion"


class OpportunityType(str, Enum):
    SURPLUS_ALLOCATION = "surplus_allocation"
    HIGH_YIELD_SAVINGS = "high_yield_savings"
    EXPENSE_REDUCTION = "expense_reduction"
    GOAL_ACCELERATION = "goal_acceleration"
    DEBT_OPTIMIZATION = "debt_optimization"


class RiskTolerance(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


# --- Core Financial Ingestion & Entity Models ---

class Transaction(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction identifier")
    user_id: str = Field(..., description="Unique user identifier")
    account_id: str = Field(..., description="Originating account identifier")
    amount: float = Field(..., description="Transaction monetary amount (positive number)")
    currency: str = Field(default="INR", description="Currency code (ISO 4217)")
    type: TransactionType = Field(..., description="Debit or credit")
    category: TransactionCategory = Field(default=TransactionCategory.OTHER, description="Normalized category")
    description: str = Field(..., description="Raw or cleaned transaction description")
    timestamp: datetime = Field(..., description="Transaction date and time")
    source: str = Field(default="manual", description="Data source: bank_api, sms, receipt, manual, csv")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Extraction or categorization confidence")
    is_recurring: bool = Field(default=False, description="Flag indicating if identified as recurring")


class IncomeRecord(BaseModel):
    income_id: str = Field(..., description="Unique income record identifier")
    user_id: str = Field(..., description="User identifier")
    source_name: str = Field(..., description="Source or employer name")
    amount: float = Field(..., description="Monetary income amount")
    currency: str = Field(default="INR", description="Currency code")
    frequency: str = Field(default="monthly", description="Frequency: monthly, biweekly, irregular")
    expected_day_of_month: Optional[int] = Field(None, ge=1, le=31, description="Expected day of arrival")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Income predictability confidence")
    variability: float = Field(default=0.0, ge=0.0, le=1.0, description="Historical variance indicator")


class Bill(BaseModel):
    bill_id: str = Field(..., description="Unique bill identifier")
    user_id: str = Field(..., description="User identifier")
    biller_name: str = Field(..., description="Biller / Payee name")
    amount: float = Field(..., description="Obligation amount")
    currency: str = Field(default="INR", description="Currency code")
    due_date: datetime = Field(..., description="Due date for payment")
    category: TransactionCategory = Field(default=TransactionCategory.UTILITIES)
    is_paid: bool = Field(default=False, description="Settlement status")
    is_auto_pay: bool = Field(default=False, description="Auto-debit status")


class Receipt(BaseModel):
    receipt_id: str = Field(..., description="Unique receipt identifier")
    user_id: str = Field(..., description="User identifier")
    merchant_name: str = Field(..., description="Merchant name")
    total_amount: float = Field(..., description="Total receipt monetary sum")
    currency: str = Field(default="INR", description="Currency code")
    timestamp: datetime = Field(..., description="Date and time of receipt")
    items: List[Dict[str, Any]] = Field(default_factory=list, description="Itemized receipt line items")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="OCR/parsing extraction confidence")


class InvestmentRecord(BaseModel):
    investment_id: str = Field(..., description="Unique investment asset identifier")
    user_id: str = Field(..., description="User identifier")
    asset_name: str = Field(..., description="Name of the asset / fund / stock")
    asset_type: str = Field(..., description="Type: mutual_fund, equity, fixed_deposit, gold, crypto")
    current_value: float = Field(..., description="Current marked-to-market valuation")
    total_invested: float = Field(..., description="Principal amount invested")
    currency: str = Field(default="INR", description="Currency code")
    monthly_sip_amount: float = Field(default=0.0, description="Recurring monthly systematic investment")
    liquidity_rating: str = Field(default="medium", description="Liquidity availability: high, medium, low")


class FinancialGoal(BaseModel):
    goal_id: str = Field(..., description="Unique financial goal identifier")
    user_id: str = Field(..., description="User identifier")
    title: str = Field(..., description="Goal name or description")
    target_amount: float = Field(..., description="Target monetary amount")
    current_amount: float = Field(default=0.0, description="Accumulated funds toward target")
    currency: str = Field(default="INR", description="Currency code")
    target_date: datetime = Field(..., description="Target achievement deadline")
    monthly_contribution_required: float = Field(default=0.0, description="Deterministic calculated monthly contribution")
    priority: int = Field(default=1, ge=1, le=5, description="Priority rank: 1 (highest) to 5 (lowest)")
    status: str = Field(default="on_track", description="Status: on_track, behind, at_risk, achieved")


class UserPreferences(BaseModel):
    user_id: str = Field(..., description="User identifier")
    risk_tolerance: RiskTolerance = Field(default=RiskTolerance.MODERATE, description="User investment risk profile")
    minimum_cash_buffer: float = Field(default=25000.0, description="User's preferred minimum bank balance reserve")
    target_emergency_fund_months: float = Field(default=3.0, description="Target emergency reserve in months of fixed expenses")
    monthly_savings_target: float = Field(default=15000.0, description="Target monthly savings quota")
    financial_priorities: List[str] = Field(
        default_factory=lambda: ["liquidity_preservation", "emergency_fund", "debt_reduction", "investments"],
        description="Ranked list of strategic financial objectives"
    )


# --- Normalized Financial Events ---

class FinancialEvent(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")
    user_id: str = Field(..., description="User identifier")
    event_type: str = Field(..., description="Event type: transaction_created, bill_due, income_received, anomaly_detected")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event occurrence timestamp")
    source: str = Field(default="manual", description="Source channel: bank_feed, sms, receipt_ocr, manual, rule_engine")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Data reliability confidence score")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Event specific details or wrapped entity")
    transaction: Optional[Transaction] = Field(None, description="Optional attached transaction entity")


# --- Derived Analytics & Signals ---

class RiskSignal(BaseModel):
    signal_id: str = Field(..., description="Unique signal identifier")
    type: RiskType = Field(..., description="Category of identified risk")
    severity: RiskSeverity = Field(..., description="Risk severity tier")
    title: str = Field(..., description="Concise human-readable risk headline")
    description: str = Field(..., description="Detailed description of the risk trigger")
    amount_impact: Optional[float] = Field(None, description="Monetary deficit or exposure amount")
    detected_at: datetime = Field(default_factory=datetime.utcnow, description="Detection timestamp")
    is_active: bool = Field(default=True, description="Active status indicator")


class OpportunitySignal(BaseModel):
    opportunity_id: str = Field(..., description="Unique opportunity identifier")
    type: OpportunityType = Field(..., description="Category of identified opportunity")
    title: str = Field(..., description="Concise opportunity headline")
    description: str = Field(..., description="Explanation of the financial upside")
    potential_benefit_amount: Optional[float] = Field(None, description="Estimated monetary savings or return")
    detected_at: datetime = Field(default_factory=datetime.utcnow, description="Detection timestamp")


class ForecastPoint(BaseModel):
    date: str = Field(..., description="Date formatted as YYYY-MM-DD")
    projected_balance: float = Field(..., description="Forecasted end-of-day bank balance")
    lower_bound: float = Field(..., description="Conservative lower estimate under uncertainty")
    upper_bound: float = Field(..., description="Optimistic upper estimate")
    is_below_buffer: bool = Field(default=False, description="Flag if projected balance violates minimum cash buffer")


class Forecast(BaseModel):
    user_id: str = Field(..., description="User identifier")
    horizon_days: int = Field(default=30, description="Forecast window duration in days")
    projected_end_balance: float = Field(..., description="Projected balance at end of horizon")
    minimum_projected_balance: float = Field(..., description="Lowest balance during the horizon window")
    lowest_balance_date: Optional[str] = Field(None, description="Date when balance reaches its minimum")
    projection_points: List[ForecastPoint] = Field(default_factory=list, description="Time-series projection curve")
    confidence: float = Field(default=0.85, ge=0.0, le=1.0, description="Confidence rating of forecast")


# --- Canonical Financial State ---

class FinancialState(BaseModel):
    user_id: str = Field(..., description="User identifier")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="State computation timestamp")
    current_balance: float = Field(..., description="Aggregate current liquid balance across checking/savings accounts")
    available_cash: float = Field(..., description="Liquid cash available after deducting immediate due obligations")
    expected_monthly_income: float = Field(..., description="Deterministic sum of recurring expected monthly income")
    income_variability: float = Field(default=0.0, description="Variability metric of income stream")
    income_confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence in upcoming income arrival")
    fixed_expenses: float = Field(..., description="Monthly fixed expenses (rent, utilities, loans, commitments)")
    variable_expenses: float = Field(..., description="Recent average monthly variable expenses (groceries, transport)")
    discretionary_expenses: float = Field(..., description="Recent average discretionary spend (dining, shopping)")
    recurring_obligations: float = Field(..., description="Total committed upcoming recurring liabilities for the month")
    upcoming_obligations: float = Field(..., description="Sum of specific unpaid bills due in the next 30 days")
    savings: float = Field(default=0.0, description="Liquid savings excluding active investment principal")
    emergency_fund_months: float = Field(default=0.0, description="Emergency fund coverage expressed in months of fixed costs")
    savings_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Proportion of monthly net income saved")
    financial_goals: List[FinancialGoal] = Field(default_factory=list, description="Active user financial goals")
    investments_total_value: float = Field(default=0.0, description="Total current market valuation of investment portfolio")
    projected_balance: float = Field(..., description="Deterministic 30-day projected end-of-month cash balance")
    minimum_cash_buffer: float = Field(default=25000.0, description="User's required minimum liquidity floor")
    risk_signals: List[RiskSignal] = Field(default_factory=list, description="Active deterministic risk signals")
    opportunity_signals: List[OpportunitySignal] = Field(default_factory=list, description="Active opportunity signals")
    user_preferences: Optional[UserPreferences] = Field(None, description="Configured user preferences")
    data_completeness: float = Field(default=1.0, ge=0.0, le=1.0, description="Ratio of required data points present")
    overall_confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Calculated aggregate system confidence")


# --- Evidence and Explainable Recommendations ---

class Evidence(BaseModel):
    metric: str = Field(..., description="Canonical metric name, e.g. projected_balance, minimum_cash_buffer")
    value: Any = Field(..., description="Calculated deterministic metric value")
    threshold: Optional[Any] = Field(None, description="Comparison threshold or benchmark value")
    status: UncertaintyStatus = Field(default=UncertaintyStatus.CONFIRMED, description="Certainty level of the metric")
    description: Optional[str] = Field(None, description="Concise context regarding metric significance")


class Recommendation(BaseModel):
    recommendation_id: str = Field(..., description="Unique recommendation identifier")
    title: str = Field(..., description="Action-oriented summary title")
    priority: str = Field(..., description="Urgency: critical, high, medium, low")
    description: str = Field(..., description="Clear explanation of the recommended action")
    impact_amount: Optional[float] = Field(None, description="Quantified monetary impact or savings")
    category: str = Field(default="liquidity", description="Category: liquidity, savings, investment, debt, budgeting")


class AgentRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    trigger_event: Optional[FinancialEvent] = Field(None, description="Optional incoming event triggering analysis")
    user_query: Optional[str] = Field(None, description="Optional natural language query from user")
    financial_state: Optional[FinancialState] = Field(None, description="Optional pre-computed state payload")


class AgentResponse(BaseModel):
    response_id: str = Field(..., description="Unique analysis response identifier")
    user_id: str = Field(..., description="User identifier")
    recommendation: Recommendation = Field(..., description="Primary prioritized recommendation")
    reason: str = Field(..., description="Explainable rationale grounded in deterministic evidence")
    evidence: List[Evidence] = Field(default_factory=list, description="Specific factual metrics supporting recommendation")
    confidence: float = Field(..., ge=0.0, le=1.0, description="System confidence score for this recommendation")
    alternatives: List[str] = Field(default_factory=list, description="Actionable alternative options for the user")
    competing_objectives_considered: List[str] = Field(
        default_factory=list,
        description="Summary of tradeoffs evaluated, e.g., liquidity preservation vs investment yield"
    )
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis completion timestamp")


# --- What-If Simulation Contracts ---

class SimulationRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    scenario_type: str = Field(..., description="Type: unexpected_expense, income_change, expense_reduction, investment_sip")
    amount: float = Field(..., description="Simulated monetary delta")
    effective_date: Optional[str] = Field(None, description="Target effective date YYYY-MM-DD")
    description: Optional[str] = Field(None, description="Contextual scenario description")


class SimulationResult(BaseModel):
    user_id: str = Field(..., description="User identifier")
    scenario_type: str = Field(..., description="Simulated scenario")
    baseline_projected_balance: float = Field(..., description="Projected balance prior to scenario")
    simulated_projected_balance: float = Field(..., description="Projected balance after scenario applied")
    buffer_violation_risk: bool = Field(..., description="True if scenario breaches minimum cash buffer")
    impact_summary: str = Field(..., description="Deterministic summary of financial impact")
    goal_impacts: List[Dict[str, Any]] = Field(default_factory=list, description="Impact on active goal completion timelines")
    recommendation: Optional[str] = Field(None, description="Agent decision guidance for this simulation")


# --- Dashboard and API Aggregates ---

class DashboardResponse(BaseModel):
    user_id: str = Field(..., description="User identifier")
    financial_state: FinancialState = Field(..., description="Current canonical financial state")
    latest_recommendation: Optional[AgentResponse] = Field(None, description="Latest AI advisor recommendation")
    recent_transactions: List[Transaction] = Field(default_factory=list, description="Recent transaction ledger")
    active_risks: List[RiskSignal] = Field(default_factory=list, description="Active risk alerts")
    active_opportunities: List[OpportunitySignal] = Field(default_factory=list, description="Active opportunities")
    forecast_30_days: Optional[Forecast] = Field(None, description="30-day deterministic balance forecast")


class APIError(BaseModel):
    error_code: str = Field(..., description="Machine-readable error classification code")
    message: str = Field(..., description="Human-readable error explanation")
    details: Optional[Dict[str, Any]] = Field(None, description="Contextual validation or execution details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
