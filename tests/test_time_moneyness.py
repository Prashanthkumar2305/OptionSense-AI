from datetime import datetime

import pytest

from backend.quant.time_moneyness import (
    TimeMoneynessFeatures,
    calculate_time_moneyness_features,
)


def test_atm_option() -> None:
    current_time = datetime(2026, 8, 6, 10, 0)
    expiry_time = datetime(2026, 8, 6, 15, 30)

    result = calculate_time_moneyness_features(
        spot_price=25_000,
        strike_price=25_000,
        current_time=current_time,
        expiry_time=expiry_time,
    )

    assert isinstance(result, TimeMoneynessFeatures)
    assert result.days_to_expiry == pytest.approx(5.5 / 24)
    assert result.hours_to_expiry == pytest.approx(5.5)
    assert result.moneyness == pytest.approx(1.0)
    assert result.distance_from_atm_pct == pytest.approx(0.0)
    assert result.is_atm is True
    assert result.is_expiry_day is True


def test_otm_option() -> None:
    current_time = datetime(2026, 8, 6, 10, 0)
    expiry_time = datetime(2026, 8, 13, 15, 30)

    result = calculate_time_moneyness_features(
        spot_price=25_000,
        strike_price=25_500,
        current_time=current_time,
        expiry_time=expiry_time,
    )

    assert result.moneyness == pytest.approx(25_000 / 25_500)
    assert result.distance_from_atm_pct == pytest.approx(-500 / 25_500 * 100)
    assert result.is_atm is False
    assert result.is_expiry_day is False


def test_custom_atm_tolerance() -> None:
    current_time = datetime(2026, 8, 6, 10, 0)
    expiry_time = datetime(2026, 8, 13, 15, 30)

    result = calculate_time_moneyness_features(
        spot_price=25_000,
        strike_price=25_500,
        current_time=current_time,
        expiry_time=expiry_time,
        atm_tolerance_pct=2.0,
    )

    assert result.is_atm is True


def test_expiry_time_equal_current_time() -> None:
    current_time = datetime(2026, 8, 6, 15, 30)

    result = calculate_time_moneyness_features(
        spot_price=25_000,
        strike_price=25_000,
        current_time=current_time,
        expiry_time=current_time,
    )

    assert result.hours_to_expiry == pytest.approx(0.0)
    assert result.days_to_expiry == pytest.approx(0.0)
    assert result.is_expiry_day is True


def test_expired_option_is_rejected() -> None:
    current_time = datetime(2026, 8, 7, 10, 0)
    expiry_time = datetime(2026, 8, 6, 15, 30)

    with pytest.raises(ValueError):
        calculate_time_moneyness_features(
            spot_price=25_000,
            strike_price=25_000,
            current_time=current_time,
            expiry_time=expiry_time,
        )


@pytest.mark.parametrize(
    "spot_price, strike_price",
    [
        (0, 25_000),
        (-100, 25_000),
        (25_000, 0),
        (25_000, -100),
    ],
)
def test_invalid_prices_are_rejected(
    spot_price: float,
    strike_price: float,
) -> None:

    current_time = datetime(2026, 8, 6, 10, 0)
    expiry_time = datetime(2026, 8, 13, 15, 30)

    with pytest.raises(ValueError):
        calculate_time_moneyness_features(
            spot_price=spot_price,
            strike_price=strike_price,
            current_time=current_time,
            expiry_time=expiry_time,
        )
