from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TimeMoneynessFeatures:
    """Time-to-expiry and option moneyness features."""

    days_to_expiry: float
    hours_to_expiry: float
    moneyness: float
    distance_from_atm_pct: float
    is_atm: bool
    is_expiry_day: bool


def calculate_time_moneyness_features(
    spot_price: float,
    strike_price: float,
    current_time: datetime,
    expiry_time: datetime,
    atm_tolerance_pct: float = 1.0,
) -> TimeMoneynessFeatures:
    """Calculate time-to-expiry and moneyness features."""

    if spot_price <= 0:
        raise ValueError("Spot_price must be greater than zero.")

    if strike_price <= 0:
        raise ValueError("strike_price must be greater than zero.")

    if expiry_time < current_time:
        raise ValueError("Expiry_time cannot be before current_time.")

    if atm_tolerance_pct < 0:
        raise ValueError("Atm_tolerance_pct cannot be negative.")

    time_difference = expiry_time - current_time

    total_hours = time_difference.total_seconds() / 3600

    days_to_expiry = total_hours / 24

    moneyness = spot_price / strike_price

    distance_from_atm_pct = ((spot_price - strike_price) / strike_price) * 100

    is_atm = abs(distance_from_atm_pct) <= atm_tolerance_pct

    is_expiry_day = current_time.date() == expiry_time.date()

    return TimeMoneynessFeatures(
        days_to_expiry=days_to_expiry,
        hours_to_expiry=total_hours,
        moneyness=moneyness,
        distance_from_atm_pct=distance_from_atm_pct,
        is_atm=is_atm,
        is_expiry_day=is_expiry_day,
    )
