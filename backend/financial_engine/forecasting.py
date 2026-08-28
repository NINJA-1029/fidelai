from datetime import datetime, timedelta
from typing import List, Optional
from shared.contracts.contracts import Forecast, ForecastPoint, FinancialState, Bill


class BalanceForecaster:
    """
    Computes deterministic 30-day balance trajectories.
    """

    @staticmethod
    def forecast_30_days(
        state: FinancialState,
        scheduled_bills: Optional[List[Bill]] = None,
        daily_discretionary_burn: Optional[float] = None
    ) -> Forecast:
        if daily_discretionary_burn is None:
            daily_discretionary_burn = (state.variable_expenses + state.discretionary_expenses) / 30.0

        points: List[ForecastPoint] = []
        running_balance = state.current_balance
        min_balance = running_balance
        lowest_date_str = None

        today = datetime.utcnow()

        for day in range(30):
            current_date = today + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")

            # Deduct daily variable burn
            running_balance -= daily_discretionary_burn

            # Deduct scheduled bill if due on this day
            if scheduled_bills:
                for b in scheduled_bills:
                    if not b.is_paid and b.due_date.date() == current_date.date():
                        running_balance -= b.amount

            # Check for income arrival (e.g. 1st or 28th of month)
            if current_date.day == 1:
                running_balance += state.expected_monthly_income

            lower_bound = running_balance * 0.95
            upper_bound = running_balance * 1.05
            is_below_buffer = running_balance < state.minimum_cash_buffer

            if running_balance < min_balance:
                min_balance = running_balance
                lowest_date_str = date_str

            points.append(
                ForecastPoint(
                    date=date_str,
                    projected_balance=round(running_balance, 2),
                    lower_bound=round(lower_bound, 2),
                    upper_bound=round(upper_bound, 2),
                    is_below_buffer=is_below_buffer
                )
            )

        return Forecast(
            user_id=state.user_id,
            horizon_days=30,
            projected_end_balance=round(points[-1].projected_balance if points else running_balance, 2),
            minimum_projected_balance=round(min_balance, 2),
            lowest_balance_date=lowest_date_str,
            projection_points=points,
            confidence=0.88
        )
