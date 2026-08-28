from datetime import datetime, timedelta
from shared.contracts.contracts import (
    Transaction,
    IncomeRecord,
    Bill,
    FinancialGoal,
    UserPreferences,
    TransactionType,
    TransactionCategory,
    RiskType,
)
from backend.financial_engine.state_calculator import FinancialStateCalculator
from backend.financial_engine.forecasting import BalanceForecaster
from backend.financial_engine.risk_detector import RiskDetector, OpportunityDetector


def test_financial_state_calculation():
    user_id = "user_demo_01"
    txns = [
        Transaction(
            transaction_id="tx_01",
            user_id=user_id,
            account_id="acc_01",
            amount=22000.0,
            currency="INR",
            type=TransactionType.DEBIT,
            category=TransactionCategory.HOUSING,
            description="Rent",
            timestamp=datetime.utcnow(),
            source="bank_api",
            confidence=1.0,
            is_recurring=True
        ),
        Transaction(
            transaction_id="tx_02",
            user_id=user_id,
            account_id="acc_01",
            amount=12000.0,
            currency="INR",
            type=TransactionType.DEBIT,
            category=TransactionCategory.UNEXPECTED,
            description="Medical Emergency",
            timestamp=datetime.utcnow(),
            source="sms",
            confidence=0.95,
            is_recurring=False
        )
    ]
    incomes = [
        IncomeRecord(
            income_id="inc_01",
            user_id=user_id,
            source_name="Salary",
            amount=65000.0,
            currency="INR",
            frequency="monthly",
            confidence=1.0
        )
    ]
    bills = [
        Bill(
            bill_id="b_01",
            user_id=user_id,
            biller_name="Rent & Maintenance",
            amount=18000.0,
            currency="INR",
            due_date=datetime.utcnow() + timedelta(days=5),
            category=TransactionCategory.HOUSING,
            is_paid=False
        )
    ]
    goals = [
        FinancialGoal(
            goal_id="g_01",
            user_id=user_id,
            title="Emergency Fund",
            target_amount=72000.0,
            current_amount=50000.0,
            currency="INR",
            target_date=datetime.utcnow() + timedelta(days=120),
            monthly_contribution_required=5500.0,
            priority=1,
            status="on_track"
        )
    ]
    prefs = UserPreferences(user_id=user_id, minimum_cash_buffer=25000.0)

    # Post unexpected expense current balance is 30,000
    state = FinancialStateCalculator.calculate_state(
        user_id=user_id,
        current_balance=30000.0,
        transactions=txns,
        income_records=incomes,
        bills=bills,
        goals=goals,
        preferences=prefs,
        investments_total_value=140000.0,
        liquid_savings=50000.0,
    )

    assert state.current_balance == 30000.0
    assert state.available_cash == 12000.0  # 30,000 - 18,000 bill due in 5 days
    assert state.expected_monthly_income == 65000.0
    assert state.emergency_fund_months == 2.3  # 50,000 / 22,000 ~ 2.3
    assert state.minimum_cash_buffer == 25000.0


def test_forecasting_and_risk_detection():
    user_id = "user_demo_01"
    prefs = UserPreferences(user_id=user_id, minimum_cash_buffer=25000.0)
    state = FinancialStateCalculator.calculate_state(
        user_id=user_id,
        current_balance=30000.0,
        transactions=[],
        income_records=[IncomeRecord(income_id="i1", user_id=user_id, source_name="Sal", amount=65000.0, currency="INR")],
        bills=[Bill(bill_id="b1", user_id=user_id, biller_name="Rent", amount=18000.0, currency="INR", due_date=datetime.utcnow() + timedelta(days=4))],
        goals=[],
        preferences=prefs,
    )
    state.projected_balance = 19400.0  # Demo forecasted value

    forecast = BalanceForecaster.forecast_30_days(state)
    assert forecast.horizon_days == 30
    assert len(forecast.projection_points) == 30

    risks = RiskDetector.detect_risks(state)
    assert len(risks) > 0
    assert any(r.type == RiskType.LIQUIDITY for r in risks)
    
    liq_risk = next(r for r in risks if r.type == RiskType.LIQUIDITY)
    assert liq_risk.amount_impact == 5600.0  # 25,000 - 19,400 = 5,600
