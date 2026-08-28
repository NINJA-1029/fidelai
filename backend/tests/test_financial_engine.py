from datetime import datetime, timedelta, timezone
from shared.contracts.contracts import (
    FinancialState,
    Transaction,
    IncomeRecord,
    Bill,
    FinancialGoal,
    UserPreferences,
    TransactionType,
    TransactionCategory,
    RiskType,
    OpportunityType,
)
from backend.financial_engine.state_calculator import FinancialStateCalculator
from backend.financial_engine.forecasting import BalanceForecaster
from backend.financial_engine.risk_detector import RiskDetector, OpportunityDetector


def test_financial_state_calculation():
    user_id = "user_demo_01"
    now = datetime.now(timezone.utc)
    
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
            timestamp=now - timedelta(days=25),
            source="bank_api",
            confidence=1.0,
            is_recurring=True,
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
            timestamp=now,
            source="sms",
            confidence=0.95,
            is_recurring=False,
        ),
        Transaction(
            transaction_id="tx_03",
            user_id=user_id,
            account_id="acc_01",
            amount=9000.0,
            currency="INR",
            type=TransactionType.DEBIT,
            category=TransactionCategory.GROCERIES,
            description="Supermarket",
            timestamp=now - timedelta(days=15),
            source="receipt",
            confidence=0.95,
            is_recurring=False,
        ),
        Transaction(
            transaction_id="tx_04",
            user_id=user_id,
            account_id="acc_01",
            amount=4000.0,
            currency="INR",
            type=TransactionType.DEBIT,
            category=TransactionCategory.DINING,
            description="Restaurants",
            timestamp=now - timedelta(days=5),
            source="bank_api",
            confidence=1.0,
            is_recurring=False,
        ),
    ]
    incomes = [
        IncomeRecord(
            income_id="inc_01",
            user_id=user_id,
            source_name="Tech Corp Salary",
            amount=65000.0,
            currency="INR",
            frequency="monthly",
            confidence=1.0,
            variability=0.05,
        )
    ]
    bills = [
        Bill(
            bill_id="b_01",
            user_id=user_id,
            biller_name="Rent & Maintenance",
            amount=18000.0,
            currency="INR",
            due_date=now + timedelta(days=5),
            category=TransactionCategory.HOUSING,
            is_paid=False,
        ),
        Bill(
            bill_id="b_02",
            user_id=user_id,
            biller_name="Internet Broadband",
            amount=1500.0,
            currency="INR",
            due_date=now + timedelta(days=20),
            category=TransactionCategory.UTILITIES,
            is_paid=False,
        ),
    ]
    goals = [
        FinancialGoal(
            goal_id="g_01",
            user_id=user_id,
            title="Emergency Fund",
            target_amount=72000.0,
            current_amount=50000.0,
            currency="INR",
            target_date=now + timedelta(days=120),
            monthly_contribution_required=5500.0,
            priority=1,
            status="on_track",
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
        as_of=now,
    )

    assert state.current_balance == 30000.0
    assert state.available_cash == 12000.0  # 30,000 - 18,000 bill due in 5 days (ignores 1500 due in 20 days)
    assert state.expected_monthly_income == 65000.0
    assert state.fixed_expenses == 22000.0
    assert state.variable_expenses == 9000.0
    assert state.discretionary_expenses == 4000.0
    assert state.upcoming_obligations == 19500.0  # 18000 + 1500
    assert state.emergency_fund_months == 2.3  # 50,000 / 22,000 ~ 2.27 -> 2.3
    assert state.minimum_cash_buffer == 25000.0
    assert state.savings_rate > 0.40
    assert state.data_completeness >= 0.90
    assert state.overall_confidence >= 0.90
    assert len(state.financial_goals) == 1
    assert state.financial_goals[0].status == "on_track"


def test_income_frequency_conversions():
    user_id = "user_freq_test"
    
    # Biweekly income
    incomes_biweekly = [
        IncomeRecord(income_id="i1", user_id=user_id, source_name="Client A", amount=30000.0, frequency="biweekly")
    ]
    s1 = FinancialStateCalculator.calculate_state(
        user_id=user_id, current_balance=10000.0, transactions=[], income_records=incomes_biweekly, bills=[], goals=[]
    )
    assert s1.expected_monthly_income == 65000.0  # 30000 * 26 / 12 = 65000.0

    # Weekly income
    incomes_weekly = [
        IncomeRecord(income_id="i2", user_id=user_id, source_name="Client B", amount=15000.0, frequency="weekly")
    ]
    s2 = FinancialStateCalculator.calculate_state(
        user_id=user_id, current_balance=10000.0, transactions=[], income_records=incomes_weekly, bills=[], goals=[]
    )
    assert s2.expected_monthly_income == 65000.0  # 15000 * 52 / 12 = 65000.0

    # Annual bonus
    incomes_annual = [
        IncomeRecord(income_id="i3", user_id=user_id, source_name="Annual Bonus", amount=120000.0, frequency="annual")
    ]
    s3 = FinancialStateCalculator.calculate_state(
        user_id=user_id, current_balance=10000.0, transactions=[], income_records=incomes_annual, bills=[], goals=[]
    )
    assert s3.expected_monthly_income == 10000.0


def test_income_fallback_from_transactions():
    user_id = "user_no_income_record"
    now = datetime.now(timezone.utc)
    
    txns = [
        Transaction(
            transaction_id="t1",
            user_id=user_id,
            account_id="acc1",
            amount=50000.0,
            currency="INR",
            type=TransactionType.CREDIT,
            category=TransactionCategory.INCOME,
            description="Consulting Credit",
            timestamp=now,
            confidence=0.92,
        )
    ]
    state = FinancialStateCalculator.calculate_state(
        user_id=user_id,
        current_balance=20000.0,
        transactions=txns,
        income_records=[],
        bills=[],
        goals=[],
    )
    assert state.expected_monthly_income == 50000.0
    assert state.income_confidence == 0.92


def test_goal_pacing_and_recalibration():
    user_id = "user_goals_test"
    now = datetime.now(timezone.utc)
    
    # 1. Goal with 4 months remaining (120 days) needing 22,000 -> ~5,500/mo
    # Surplus is 65,000 - 35,000 = 30,000 -> on_track
    g1 = FinancialGoal(
        goal_id="g1",
        user_id=user_id,
        title="Emergency Reserve",
        target_amount=72000.0,
        current_amount=50000.0,
        currency="INR",
        target_date=now + timedelta(days=120),
    )
    # 2. Already achieved goal
    g2 = FinancialGoal(
        goal_id="g2",
        user_id=user_id,
        title="Laptop Fund",
        target_amount=80000.0,
        current_amount=80000.0,
        currency="INR",
        target_date=now + timedelta(days=60),
    )
    
    incomes = [IncomeRecord(income_id="i1", user_id=user_id, source_name="Sal", amount=65000.0, frequency="monthly")]
    
    state = FinancialStateCalculator.calculate_state(
        user_id=user_id,
        current_balance=50000.0,
        transactions=[],
        income_records=incomes,
        bills=[],
        goals=[g1, g2],
        as_of=now,
    )
    
    assert len(state.financial_goals) == 2
    assert state.financial_goals[0].monthly_contribution_required == 5500.0
    assert state.financial_goals[0].status == "on_track"
    assert state.financial_goals[1].monthly_contribution_required == 0.0
    assert state.financial_goals[1].status == "achieved"


def test_available_cash_and_immediate_bills():
    user_id = "user_cash_test"
    now = datetime.now(timezone.utc)
    
    bills = [
        # Due in 3 days (Immediate)
        Bill(bill_id="b1", user_id=user_id, biller_name="Rent", amount=15000.0, due_date=now + timedelta(days=3), is_paid=False),
        # Due in 6 days (Immediate)
        Bill(bill_id="b2", user_id=user_id, biller_name="Power", amount=3000.0, due_date=now + timedelta(days=6), is_paid=False),
        # Due in 15 days (Non-immediate upcoming)
        Bill(bill_id="b3", user_id=user_id, biller_name="Loan", amount=8000.0, due_date=now + timedelta(days=15), is_paid=False),
        # Already paid bill
        Bill(bill_id="b4", user_id=user_id, biller_name="Wifi", amount=1000.0, due_date=now + timedelta(days=2), is_paid=True),
    ]
    
    state = FinancialStateCalculator.calculate_state(
        user_id=user_id,
        current_balance=25000.0,
        transactions=[],
        income_records=[],
        bills=bills,
        goals=[],
        as_of=now,
    )
    
    # Available cash deducts only unpaid bills due in <= 7 days: 25000 - 15000 - 3000 = 7000
    assert state.available_cash == 7000.0
    # Upcoming obligations sums all unpaid bills due in <= 30 days: 15000 + 3000 + 8000 = 26000
    assert state.upcoming_obligations == 26000.0


def test_signals_hydration_in_state():
    user_id = "user_signal_test"
    now = datetime.now(timezone.utc)
    
    prefs = UserPreferences(user_id=user_id, minimum_cash_buffer=25000.0)
    bills = [Bill(bill_id="b1", user_id=user_id, biller_name="Rent", amount=20000.0, due_date=now + timedelta(days=5), is_paid=False)]
    
    state = FinancialStateCalculator.calculate_state(
        user_id=user_id,
        current_balance=22000.0,
        transactions=[],
        income_records=[IncomeRecord(income_id="i1", user_id=user_id, source_name="Sal", amount=40000.0)],
        bills=bills,
        goals=[],
        preferences=prefs,
        liquid_savings=10000.0,
        populate_signals=True,
    )
    
    assert len(state.risk_signals) > 0
    assert any(r.type == RiskType.LIQUIDITY for r in state.risk_signals)


def test_forecasting_daily_burn_and_bill_settlements():
    user_id = "user_forecast_test"
    now = datetime(2026, 8, 1, 0, 0, tzinfo=timezone.utc)
    
    state = FinancialState(
        user_id=user_id,
        generated_at=now,
        current_balance=50000.0,
        available_cash=30000.0,
        expected_monthly_income=60000.0,
        income_variability=0.05,
        income_confidence=0.95,
        fixed_expenses=20000.0,
        variable_expenses=15000.0,
        discretionary_expenses=15000.0,
        recurring_obligations=20000.0,
        upcoming_obligations=20000.0,
        savings=30000.0,
        emergency_fund_months=1.5,
        savings_rate=0.15,
        financial_goals=[],
        investments_total_value=0.0,
        projected_balance=35000.0,
        minimum_cash_buffer=25000.0,
        risk_signals=[],
        opportunity_signals=[],
    )
    
    bills = [
        Bill(bill_id="b1", user_id=user_id, biller_name="Rent", amount=20000.0, due_date=now + timedelta(days=5), is_paid=False)
    ]
    
    forecast = BalanceForecaster.forecast_30_days(state, scheduled_bills=bills, start_date=now)
    assert forecast.horizon_days == 30
    assert len(forecast.projection_points) == 30
    
    # Check day 0: daily burn deducted: 50,000 - (30,000/30 = 1000) = 49,000
    assert forecast.projection_points[0].projected_balance == 49000.0
    
    # Check day 5: bill deducted
    assert forecast.projection_points[5].projected_balance < 29000.0


def test_forecasting_shock_simulation():
    user_id = "user_shock_test"
    now = datetime(2026, 8, 1, 0, 0, tzinfo=timezone.utc)
    
    state = FinancialState(
        user_id=user_id,
        generated_at=now,
        current_balance=50000.0,
        available_cash=40000.0,
        expected_monthly_income=60000.0,
        income_variability=0.05,
        income_confidence=0.95,
        fixed_expenses=20000.0,
        variable_expenses=15000.0,
        discretionary_expenses=15000.0,
        recurring_obligations=20000.0,
        upcoming_obligations=0.0,
        savings=30000.0,
        emergency_fund_months=1.5,
        savings_rate=0.15,
        financial_goals=[],
        investments_total_value=0.0,
        projected_balance=35000.0,
        minimum_cash_buffer=25000.0,
        risk_signals=[],
        opportunity_signals=[],
    )
    
    shock_forecast = BalanceForecaster.simulate_shock(state, shock_amount=15000.0, effective_day=0)
    assert shock_forecast.projection_points[0].projected_balance == 34000.0  # (50k - 15k) - 1k daily burn


def test_risk_triggers_comprehensive():
    user_id = "user_risk_suite"
    now = datetime.now(timezone.utc)
    
    # State with multiple risk indicators:
    # 1. Liquidity deficit (projected 15k < buffer 25k)
    # 2. Upcoming obligation gap (cash 5k < bills 18k)
    # 3. Emergency fund depletion (< 1.0 month)
    # 4. Spending spike (discretionary 16k)
    # 5. Income volatility (variability 0.30)
    # 6. Goal deficit (goal at risk)
    state = FinancialState(
        user_id=user_id,
        generated_at=now,
        current_balance=10000.0,
        available_cash=5000.0,
        expected_monthly_income=45000.0,
        income_variability=0.30,
        income_confidence=0.65,
        fixed_expenses=22000.0,
        variable_expenses=10000.0,
        discretionary_expenses=16000.0,
        recurring_obligations=22000.0,
        upcoming_obligations=18000.0,
        savings=10000.0,
        emergency_fund_months=0.4,
        savings_rate=0.0,
        financial_goals=[
            FinancialGoal(
                goal_id="g1",
                user_id=user_id,
                title="Goal P1",
                target_amount=50000.0,
                current_amount=10000.0,
                currency="INR",
                target_date=now + timedelta(days=60),
                monthly_contribution_required=20000.0,
                priority=1,
                status="at_risk",
            )
        ],
        investments_total_value=0.0,
        projected_balance=15000.0,
        minimum_cash_buffer=25000.0,
        risk_signals=[],
        opportunity_signals=[],
        user_preferences=UserPreferences(user_id=user_id, minimum_cash_buffer=25000.0, target_emergency_fund_months=3.0),
    )
    
    risks = RiskDetector.detect_risks(state)
    risk_types = {r.type for r in risks}
    
    assert RiskType.LIQUIDITY in risk_types
    assert RiskType.UPCOMING_OBLIGATION in risk_types
    assert RiskType.EMERGENCY_FUND_DEPLETION in risk_types
    assert RiskType.SPENDING_SPIKE in risk_types
    assert RiskType.INCOME_REDUCTION in risk_types
    assert RiskType.GOAL_DEFICIT in risk_types


def test_opportunity_triggers_comprehensive():
    user_id = "user_opp_suite"
    now = datetime.now(timezone.utc)
    
    # State with opportunities:
    # 1. Expense reduction cushion (discretionary 8000 > 4000)
    # 2. Surplus allocation (projected 45k > buffer 25k + 10k)
    # 3. Goal acceleration (savings rate 35% with on_track goal)
    # 4. High-yield savings (balance 60k > buffer 25k + 25k)
    state = FinancialState(
        user_id=user_id,
        generated_at=now,
        current_balance=60000.0,
        available_cash=50000.0,
        expected_monthly_income=75000.0,
        income_variability=0.05,
        income_confidence=0.95,
        fixed_expenses=20000.0,
        variable_expenses=10000.0,
        discretionary_expenses=8000.0,
        recurring_obligations=20000.0,
        upcoming_obligations=5000.0,
        savings=50000.0,
        emergency_fund_months=2.5,
        savings_rate=0.35,
        financial_goals=[
            FinancialGoal(
                goal_id="g1",
                user_id=user_id,
                title="Vacation",
                target_amount=40000.0,
                current_amount=20000.0,
                currency="INR",
                target_date=now + timedelta(days=90),
                monthly_contribution_required=6666.0,
                priority=2,
                status="on_track",
            )
        ],
        investments_total_value=100000.0,
        projected_balance=45000.0,
        minimum_cash_buffer=25000.0,
        risk_signals=[],
        opportunity_signals=[],
        user_preferences=UserPreferences(user_id=user_id, minimum_cash_buffer=25000.0),
    )
    
    opps = OpportunityDetector.detect_opportunities(state)
    opp_types = {o.type for o in opps}
    
    assert OpportunityType.EXPENSE_REDUCTION in opp_types
    assert OpportunityType.SURPLUS_ALLOCATION in opp_types
    assert OpportunityType.GOAL_ACCELERATION in opp_types
    assert OpportunityType.HIGH_YIELD_SAVINGS in opp_types


