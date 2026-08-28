from datetime import datetime, timedelta, timezone
from typing import List, Optional
from shared.contracts.contracts import Forecast, ForecastPoint, FinancialState, Bill


class BalanceForecaster:
    """
    Authoritative deterministic trajectory calculator for cash flow and bank balance projections.
    """

    @staticmethod
    def _to_utc(dt: datetime) -> datetime:
        """Ensures a datetime is timezone-aware in UTC."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @classmethod
    def forecast_30_days(
        cls,
        state: FinancialState,
        scheduled_bills: Optional[List[Bill]] = None,
        daily_discretionary_burn: Optional[float] = None,
        horizon_days: int = 30,
        start_date: Optional[datetime] = None,
    ) -> Forecast:
        """
        Computes a deterministic 30-day daily bank balance projection curve
        with dynamic uncertainty envelopes and cash buffer monitoring.
        """
        ref_start = cls._to_utc(start_date) if start_date else cls._to_utc(state.generated_at)

        if daily_discretionary_burn is None:
            daily_discretionary_burn = (state.variable_expenses + state.discretionary_expenses) / 30.0

        points: List[ForecastPoint] = []
        running_balance = state.current_balance
        min_balance = running_balance
        lowest_date_str = ref_start.strftime("%Y-%m-%d")

        # Map scheduled unpaid bills to day of month or ISO date
        unpaid_bills = [b for b in (scheduled_bills or []) if not b.is_paid]

        for day in range(horizon_days):
            current_date = ref_start + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")

            # 1. Income arrival simulation (e.g. 1st of month)
            if current_date.day == 1 and day > 0:
                running_balance += state.expected_monthly_income

            # 2. Deduct scheduled bills due on this date
            for b in unpaid_bills:
                b_due = cls._to_utc(b.due_date)
                if b_due.date() == current_date.date():
                    running_balance -= b.amount

            # 3. Deduct daily variable & discretionary burn
            running_balance -= daily_discretionary_burn

            # 4. Dynamic uncertainty envelope
            uncertainty_factor = 0.02 + (0.003 * day) + (state.income_variability * 0.5)
            lower_bound = round(running_balance * (1.0 - uncertainty_factor), 2)
            upper_bound = round(running_balance * (1.0 + uncertainty_factor), 2)
            is_below_buffer = running_balance < state.minimum_cash_buffer

            if running_balance < min_balance:
                min_balance = running_balance
                lowest_date_str = date_str

            points.append(
                ForecastPoint(
                    date=date_str,
                    projected_balance=round(running_balance, 2),
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    is_below_buffer=is_below_buffer,
                )
            )

        projected_end = points[-1].projected_balance if points else running_balance
        confidence = round(min(0.95, max(0.65, state.overall_confidence * 0.94)), 2)

        return Forecast(
            user_id=state.user_id,
            horizon_days=horizon_days,
            projected_end_balance=round(projected_end, 2),
            minimum_projected_balance=round(min_balance, 2),
            lowest_balance_date=lowest_date_str,
            projection_points=points,
            confidence=confidence,
        )

    @classmethod
    def simulate_shock(
        cls,
        state: FinancialState,
        shock_amount: float,
        effective_day: int = 0,
        scheduled_bills: Optional[List[Bill]] = None,
    ) -> Forecast:
        """
        Generates a simulated trajectory under an immediate or scheduled financial shock.
        """
        # Create a modified state copy with adjusted current balance if effective on day 0
        modified_balance = state.current_balance - (shock_amount if effective_day == 0 else 0.0)
        simulated_state = state.model_copy(update={"current_balance": modified_balance})
        return cls.forecast_30_days(simulated_state, scheduled_bills=scheduled_bills)

